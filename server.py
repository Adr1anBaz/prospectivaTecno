import os
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

import psycopg
from mcp.server.fastmcp import FastMCP
from psycopg.rows import dict_row
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

MCP_BEARER_TOKEN = os.getenv("MCP_BEARER_TOKEN")


class BearerAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not MCP_BEARER_TOKEN:
            return await call_next(request)

        auth_header = request.headers.get("authorization", "")
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return JSONResponse(
                {"error": "unauthorized", "error_description": "Bearer token required"},
                status_code=401,
            )

        token = parts[1]
        if token != MCP_BEARER_TOKEN:
            return JSONResponse(
                {"error": "invalid_token", "error_description": "Invalid bearer token"},
                status_code=401,
            )

        return await call_next(request)


mcp = FastMCP(
    "campus-info-mcp",
    stateless_http=True,
    json_response=True,
)


def normalize(value: Any) -> Any:
    """
    Convert PostgreSQL/Python types into JSON-friendly values.
    """
    if isinstance(value, UUID):
        return str(value)

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date, time)):
        return value.isoformat()

    if isinstance(value, list):
        return [normalize(item) for item in value]

    if isinstance(value, dict):
        return {key: normalize(val) for key, val in value.items()}

    return value


def normalize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize(dict(row)) for row in rows]


def query_db(sql: str, params: tuple = ()) -> list[dict[str, Any]]:
    """
    Execute a safe read-only query.
    """
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        conn.execute("SET TRANSACTION READ ONLY;")
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return normalize_rows(rows)


@mcp.tool()
def health_check() -> dict:
    """
    Check that the MCP server can connect to the database.
    """
    result = query_db("SELECT current_database() AS database, NOW() AS checked_at;")
    return {
        "status": "ok",
        "database": result[0]["database"],
        "checked_at": result[0]["checked_at"],
    }


@mcp.tool()
def database_summary() -> dict:
    """
    Return a quick summary of the database.
    """
    total_places = query_db("SELECT COUNT(*) AS count FROM places;")
    by_type = query_db(
        """
        SELECT type, COUNT(*) AS count
        FROM places
        GROUP BY type
        ORDER BY type;
        """
    )

    return {
        "total_places": total_places[0]["count"],
        "places_by_type": by_type,
    }


@mcp.tool()
def list_places(place_type: Optional[str] = None) -> list[dict]:
    """
    List campus places. Optionally filter by type:
    restaurant, classroom, lab, store, office, department, gate, common_area.
    """
    if place_type:
        return query_db(
            """
            SELECT
                p.id,
                p.name,
                p.type,
                p.description,
                p.floor,
                p.room_code,
                p.status,
                p.metadata,
                b.name AS building_name
            FROM places p
            LEFT JOIN buildings b ON b.id = p.building_id
            WHERE p.type = %s
            ORDER BY p.name;
            """,
            (place_type,),
        )

    return query_db(
        """
        SELECT
            p.id,
            p.name,
            p.type,
            p.description,
            p.floor,
            p.room_code,
            p.status,
            p.metadata,
            b.name AS building_name
        FROM places p
        LEFT JOIN buildings b ON b.id = p.building_id
        ORDER BY p.name;
        """
    )


@mcp.tool()
def search_places(query: str) -> list[dict]:
    """
    Search places by name, description, type, room code, building name or metadata.
    """
    pattern = f"%{query}%"

    return query_db(
        """
        SELECT
            p.id,
            p.name,
            p.type,
            p.description,
            p.floor,
            p.room_code,
            p.status,
            p.metadata,
            b.name AS building_name
        FROM places p
        LEFT JOIN buildings b ON b.id = p.building_id
        WHERE
            p.name ILIKE %s
            OR p.description ILIKE %s
            OR p.type ILIKE %s
            OR p.room_code ILIKE %s
            OR p.metadata::text ILIKE %s
            OR b.name ILIKE %s
        ORDER BY p.name
        LIMIT 20;
        """,
        (pattern, pattern, pattern, pattern, pattern, pattern),
    )


@mcp.tool()
def get_place_detail(place_id: str) -> dict:
    """
    Get detailed information about a place using its place_id.
    Includes opening hours and type-specific profile when available.
    """
    places = query_db(
        """
        SELECT
            p.*,
            b.name AS building_name,
            c.name AS campus_name
        FROM places p
        LEFT JOIN buildings b ON b.id = p.building_id
        LEFT JOIN campuses c ON c.id = p.campus_id
        WHERE p.id = %s;
        """,
        (place_id,),
    )

    if not places:
        return {"error": "Place not found"}

    place = places[0]
    place_type = place["type"]

    result = {
        "place": place,
        "opening_hours": query_db(
            """
            SELECT day_of_week, opens_at, closes_at, valid_from, valid_to
            FROM opening_hours
            WHERE place_id = %s
            ORDER BY day_of_week, opens_at;
            """,
            (place_id,),
        ),
        "schedule_exceptions": query_db(
            """
            SELECT date, is_closed, opens_at, closes_at, reason
            FROM schedule_exceptions
            WHERE place_id = %s
            ORDER BY date;
            """,
            (place_id,),
        ),
    }

    if place_type == "restaurant":
        result["restaurant_profile"] = query_db(
            "SELECT * FROM restaurant_profiles WHERE place_id = %s;",
            (place_id,),
        )
        result["menus"] = get_restaurant_menu(place_id)

    elif place_type in ("classroom", "lab"):
        result["room_profile"] = query_db(
            "SELECT * FROM room_profiles WHERE place_id = %s;",
            (place_id,),
        )

    elif place_type == "store":
        result["store_profile"] = query_db(
            "SELECT * FROM store_profiles WHERE place_id = %s;",
            (place_id,),
        )
        result["products"] = get_store_products(place_id)

    elif place_type in ("office", "department"):
        result["office_profile"] = query_db(
            "SELECT * FROM office_profiles WHERE place_id = %s;",
            (place_id,),
        )

    elif place_type == "gate":
        result["gate_profile"] = query_db(
            "SELECT * FROM gate_profiles WHERE place_id = %s;",
            (place_id,),
        )

    return result


@mcp.tool()
def get_place_detail_by_name(name: str) -> dict:
    """
    Get detailed information about a place using its name.
    Useful when the user does not know the UUID.
    """
    places = query_db(
        """
        SELECT id, name, type
        FROM places
        WHERE name ILIKE %s
        ORDER BY name
        LIMIT 1;
        """,
        (f"%{name}%",),
    )

    if not places:
        return {"error": "Place not found"}

    return get_place_detail(places[0]["id"])


@mcp.tool()
def get_restaurant_menu(place_id: str) -> dict:
    """
    Get menus and menu items for a restaurant.
    """
    menus = query_db(
        """
        SELECT id, name, description, active
        FROM menus
        WHERE place_id = %s
        ORDER BY name;
        """,
        (place_id,),
    )

    result = {"menus": []}

    for menu in menus:
        items = query_db(
            """
            SELECT
                id,
                name,
                description,
                category,
                price,
                currency,
                dietary_tags,
                available,
                metadata
            FROM menu_items
            WHERE menu_id = %s
            ORDER BY category, name;
            """,
            (menu["id"],),
        )

        result["menus"].append(
            {
                "menu": menu,
                "items": items,
            }
        )

    return result


@mcp.tool()
def get_restaurant_menu_by_name(name: str) -> dict:
    """
    Get restaurant menu using the restaurant name.
    """
    places = query_db(
        """
        SELECT id, name, type
        FROM places
        WHERE type = 'restaurant'
          AND name ILIKE %s
        ORDER BY name
        LIMIT 1;
        """,
        (f"%{name}%",),
    )

    if not places:
        return {"error": "Restaurant not found"}

    return get_restaurant_menu(places[0]["id"])


@mcp.tool()
def search_food(query: str, max_price: Optional[float] = None) -> list[dict]:
    """
    Search restaurant menu items by name, description, category or dietary tags.
    Optionally filter by max price.
    """
    pattern = f"%{query}%"

    if max_price is not None:
        return query_db(
            """
            SELECT
                p.name AS restaurant_name,
                mi.name AS item_name,
                mi.description,
                mi.category,
                mi.price,
                mi.currency,
                mi.dietary_tags,
                mi.available
            FROM menu_items mi
            JOIN menus m ON m.id = mi.menu_id
            JOIN places p ON p.id = m.place_id
            WHERE
                p.type = 'restaurant'
                AND mi.available = true
                AND mi.price <= %s
                AND (
                    mi.name ILIKE %s
                    OR mi.description ILIKE %s
                    OR mi.category ILIKE %s
                    OR mi.dietary_tags::text ILIKE %s
                )
            ORDER BY mi.price ASC
            LIMIT 20;
            """,
            (max_price, pattern, pattern, pattern, pattern),
        )

    return query_db(
        """
        SELECT
            p.name AS restaurant_name,
            mi.name AS item_name,
            mi.description,
            mi.category,
            mi.price,
            mi.currency,
            mi.dietary_tags,
            mi.available
        FROM menu_items mi
        JOIN menus m ON m.id = mi.menu_id
        JOIN places p ON p.id = m.place_id
        WHERE
            p.type = 'restaurant'
            AND mi.available = true
            AND (
                mi.name ILIKE %s
                OR mi.description ILIKE %s
                OR mi.category ILIKE %s
                OR mi.dietary_tags::text ILIKE %s
            )
        ORDER BY mi.price ASC
        LIMIT 20;
        """,
        (pattern, pattern, pattern, pattern),
    )


@mcp.tool()
def get_store_products(place_id: str) -> list[dict]:
    """
    Get products for a store.
    """
    return query_db(
        """
        SELECT
            name,
            description,
            category,
            price,
            currency,
            available,
            metadata
        FROM products
        WHERE place_id = %s
        ORDER BY category, name;
        """,
        (place_id,),
    )


@mcp.tool()
def search_products(query: str, max_price: Optional[float] = None) -> list[dict]:
    """
    Search store products by name, description or category.
    Optionally filter by max price.
    """
    pattern = f"%{query}%"

    if max_price is not None:
        return query_db(
            """
            SELECT
                p.name AS store_name,
                pr.name AS product_name,
                pr.description,
                pr.category,
                pr.price,
                pr.currency,
                pr.available
            FROM products pr
            JOIN places p ON p.id = pr.place_id
            WHERE
                pr.available = true
                AND pr.price <= %s
                AND (
                    pr.name ILIKE %s
                    OR pr.description ILIKE %s
                    OR pr.category ILIKE %s
                )
            ORDER BY pr.price ASC
            LIMIT 20;
            """,
            (max_price, pattern, pattern, pattern),
        )

    return query_db(
        """
        SELECT
            p.name AS store_name,
            pr.name AS product_name,
            pr.description,
            pr.category,
            pr.price,
            pr.currency,
            pr.available
        FROM products pr
        JOIN places p ON p.id = pr.place_id
        WHERE
            pr.available = true
            AND (
                pr.name ILIKE %s
                OR pr.description ILIKE %s
                OR pr.category ILIKE %s
            )
        ORDER BY pr.price ASC
        LIMIT 20;
        """,
        (pattern, pattern, pattern),
    )


@mcp.tool()
def find_office_by_need(query: str) -> list[dict]:
    """
    Search offices/departments by purpose, department type or services.
    """
    pattern = f"%{query}%"

    return query_db(
        """
        SELECT
            p.id,
            p.name,
            p.description,
            op.department_type,
            op.purpose,
            op.services,
            op.contact_email,
            op.phone,
            op.website_url
        FROM office_profiles op
        JOIN places p ON p.id = op.place_id
        WHERE
            p.name ILIKE %s
            OR p.description ILIKE %s
            OR op.department_type ILIKE %s
            OR op.purpose ILIKE %s
            OR op.services::text ILIKE %s
        ORDER BY p.name
        LIMIT 20;
        """,
        (pattern, pattern, pattern, pattern, pattern),
    )


@mcp.tool()
def get_gates() -> list[dict]:
    """
    List campus gates with entry/exit permissions and adjacent streets.
    """
    return query_db(
        """
        SELECT
            p.id,
            p.name,
            p.description,
            gp.gate_type,
            gp.entry_allowed,
            gp.exit_allowed,
            gp.adjacent_streets,
            gp.security_notes
        FROM gate_profiles gp
        JOIN places p ON p.id = gp.place_id
        ORDER BY p.name;
        """
    )


@mcp.tool()
def search_semantic_documents(query: str) -> list[dict]:
    """
    Search semantic documents by text.
    This is temporary lexical search.
    Later it can become true vector search with embeddings.
    """
    pattern = f"%{query}%"

    return query_db(
        """
        SELECT
            entity_type,
            entity_id,
            title,
            content,
            metadata,
            embedding_model,
            updated_at
        FROM semantic_documents
        WHERE
            title ILIKE %s
            OR content ILIKE %s
            OR metadata::text ILIKE %s
        ORDER BY title
        LIMIT 20;
        """,
        (pattern, pattern, pattern),
    )


@mcp.tool()
def get_current_crowd_levels() -> list[dict]:
    """
    Get latest crowd level per place when available.
    """
    return query_db(
        """
        SELECT DISTINCT ON (p.id)
            p.id AS place_id,
            p.name AS place_name,
            cl.observed_at,
            cl.level,
            cl.percentage,
            cl.source
        FROM places p
        JOIN crowd_levels cl ON cl.place_id = p.id
        ORDER BY p.id, cl.observed_at DESC;
        """
    )


if __name__ == "__main__":
    app = mcp.streamable_http_app()
    app.add_middleware(BearerAuthMiddleware)

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
