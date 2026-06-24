import copy
from typing import Any, Dict, List, Optional
from prospectiva.utils.mcp_client import MCPClient

logger = None


class MockMCPClient(MCPClient):
    """
    Mock MCP Client for testing without the real server.
    Returns realistic fictional campus data.
    """

    def __init__(self, url: str | None = None, token: str | None = None, timeout: float = 10.0):
        self.url = "mock://localhost"
        self.token = ""
        self._available = True
        self._initialized = True
        self._server_info = {"name": "campus-info-mcp-mock", "version": "1.0"}
        self._places = self._build_places()

    def is_available(self) -> bool:
        return True

    # ── helpers ──────────────────────────────────

    def _find_place(self, place_id: str) -> dict | None:
        return next((p for p in self._places if p["id"] == place_id), None)

    def _find_place_by_name(self, name: str) -> dict | None:
        name_lower = name.lower()
        for p in self._places:
            if name_lower in p["name"].lower():
                return p
        return None

    def _places_of_type(self, place_type: str) -> list[dict]:
        return [p for p in self._places if p.get("type") == place_type]

    # ── mock data ────────────────────────────────

    def _build_places(self) -> list[dict]:
        return [
            {
                "id": "place-001",
                "name": "Restaurante Giornale",
                "type": "restaurant",
                "description": "Comida italiana, pizzas artesanales y pasta fresca.",
                "floor": 1,
                "room_code": "G-01",
                "status": "open",
                "metadata": {"cuisine": "italiana", "rating": 4.3},
                "building_name": "Edificio Principal",
            },
            {
                "id": "place-002",
                "name": "Cafetería Universitaria",
                "type": "restaurant",
                "description": "Comida económica para estudiantes.",
                "floor": 0,
                "room_code": "B-01",
                "status": "open",
                "metadata": {"cuisine": "mexicana", "rating": 4.0},
                "building_name": "Edificio de Servicios",
            },
            {
                "id": "place-003",
                "name": "Edificio de Biomédica",
                "type": "department",
                "description": "Ingeniería biomédica, laboratorios y aulas.",
                "floor": 2,
                "room_code": "BIO-01",
                "status": "open",
                "metadata": {},
                "building_name": "Edificio de Biomédica",
            },
            {
                "id": "place-004",
                "name": "Biblioteca Central",
                "type": "common_area",
                "description": "Biblioteca central con áreas de estudio y computadoras.",
                "floor": 0,
                "room_code": "LIB-01",
                "status": "open",
                "metadata": {},
                "building_name": "Edificio Cultural",
            },
            {
                "id": "place-005",
                "name": "Laboratorio de Física",
                "type": "lab",
                "description": "Laboratorio de física con equipos de óptica y mecánica.",
                "floor": 1,
                "room_code": "FIS-01",
                "status": "open",
                "metadata": {},
                "building_name": "Edificio de Ciencias",
            },
            {
                "id": "place-006",
                "name": "Tienda Universitaria",
                "type": "store",
                "description": "Papelería, uniformes y artículos de oficina.",
                "floor": 0,
                "room_code": "T-01",
                "status": "open",
                "metadata": {},
                "building_name": "Edificio de Servicios",
            },
            {
                "id": "place-007",
                "name": "Puerta Norte",
                "type": "gate",
                "description": "Acceso principal norte del campus.",
                "floor": 0,
                "room_code": "",
                "status": "open",
                "metadata": {},
                "building_name": "",
            },
        ]

    # ── tool methods ─────────────────────────────

    def health_check(self) -> dict:
        return {"status": "ok", "database": "mock_campus", "checked_at": "2026-01-01T12:00:00"}

    def database_summary(self) -> dict:
        return {
            "total_places": len(self._places),
            "places_by_type": [
                {"type": t, "count": len(self._places_of_type(t))}
                for t in set(p["type"] for p in self._places)
            ],
        }

    def list_places(self, place_type: str | None = None) -> list[dict]:
        if place_type:
            return self._places_of_type(place_type)
        return self._places

    def search_places(self, query: str) -> list[dict]:
        q = query.lower()
        results = []
        for p in self._places:
            if (q in p["name"].lower()
                    or q in p["description"].lower()
                    or q in p.get("building_name", "").lower()
                    or q in p.get("room_code", "").lower()):
                results.append(p)
        return results[:20]

    def get_place_detail(self, place_id: str) -> dict:
        place = self._find_place(place_id)
        if not place:
            return {"error": "Place not found"}
        result = {
            "place": place,
            "opening_hours": [
                {"day_of_week": 1, "opens_at": "08:00", "closes_at": "18:00", "valid_from": None, "valid_to": None},
                {"day_of_week": 2, "opens_at": "08:00", "closes_at": "18:00", "valid_from": None, "valid_to": None},
            ],
            "schedule_exceptions": [],
        }
        if place["type"] == "restaurant":
            result["restaurant_profile"] = [{"place_id": place_id, "cuisine_type": "variada"}]
            result["menus"] = {
                "menus": [{
                    "menu": {"id": "menu-001", "name": "Menú del Día", "description": "Platillo del día", "active": True},
                    "items": [
                        {"id": "item-001", "name": "Pizza", "description": "Pizza artesanal", "category": "principal",
                         "price": 45.0, "currency": "MXN", "dietary_tags": ["vegetariana"], "available": True},
                        {"id": "item-002", "name": "Ensalada", "description": "Ensalada fresca", "category": "entrada",
                         "price": 25.0, "currency": "MXN", "dietary_tags": ["vegana"], "available": True},
                    ],
                }],
            }
        elif place["type"] in ("classroom", "lab"):
            result["room_profile"] = [{"capacity": 30, "equipment": ["proyector", "pizarrón"]}]
        elif place["type"] == "store":
            result["store_profile"] = [{"store_type": "papelería"}]
            result["products"] = [
                {"name": "Cuaderno", "category": "papelería", "price": 35.0, "currency": "MXN", "available": True},
                {"name": "Pluma", "category": "papelería", "price": 12.0, "currency": "MXN", "available": True},
            ]
        elif place["type"] in ("office", "department"):
            result["office_profile"] = [{"department_type": "académico", "purpose": "Docencia e investigación"}]
        elif place["type"] == "gate":
            result["gate_profile"] = [{"gate_type": "principal", "entry_allowed": True, "exit_allowed": True}]
        return result

    def get_place_detail_by_name(self, name: str) -> dict:
        place = self._find_place_by_name(name)
        if not place:
            return {"error": "Place not found"}
        return self.get_place_detail(place["id"])

    def get_restaurant_menu(self, place_id: str) -> dict:
        place = self._find_place(place_id)
        if not place or place["type"] != "restaurant":
            return {"error": "Restaurant not found"}
        return {
            "menus": [{
                "menu": {"id": "menu-001", "name": "Menú Principal", "active": True},
                "items": [
                    {"id": "item-001", "name": "Pizza Margherita", "category": "principal",
                     "price": 45.0, "currency": "MXN", "available": True},
                    {"id": "item-002", "name": "Ensalada César", "category": "entrada",
                     "price": 25.0, "currency": "MXN", "available": True},
                ],
            }],
        }

    def get_restaurant_menu_by_name(self, name: str) -> dict:
        place = self._find_place_by_name(name)
        if not place:
            return {"error": "Restaurant not found"}
        return self.get_restaurant_menu(place["id"])

    def search_food(self, query: str, max_price: float | None = None) -> list[dict]:
        q = query.lower()
        results = []
        for p in self._places_of_type("restaurant"):
            menu = self.get_restaurant_menu(p["id"])
            for menu_entry in menu.get("menus", []):
                for item in menu_entry.get("items", []):
                    if q in item["name"].lower() or q in item.get("description", "").lower() or q in item.get("category", "").lower():
                        if max_price is None or item["price"] <= max_price:
                            results.append({
                                "restaurant_name": p["name"],
                                "item_name": item["name"],
                                "category": item["category"],
                                "price": item["price"],
                                "currency": item["currency"],
                                "available": item["available"],
                            })
        return results[:20]

    def get_store_products(self, place_id: str) -> list[dict]:
        place = self._find_place(place_id)
        if not place or place["type"] != "store":
            return []
        return [
            {"name": "Cuaderno Profesional", "description": "Cuaderno de 100 hojas", "category": "papelería",
             "price": 35.0, "currency": "MXN", "available": True},
            {"name": "Pluma Tinta Azul", "description": "Pluma de gel", "category": "papelería",
             "price": 12.0, "currency": "MXN", "available": True},
        ]

    def search_products(self, query: str, max_price: float | None = None) -> list[dict]:
        q = query.lower()
        results = []
        for p in self._places_of_type("store"):
            products = self.get_store_products(p["id"])
            for pr in products:
                if q in pr["name"].lower() or q in pr.get("description", "").lower():
                    if max_price is None or pr["price"] <= max_price:
                        results.append({
                            "store_name": p["name"],
                            "product_name": pr["name"],
                            "category": pr["category"],
                            "price": pr["price"],
                            "currency": pr["currency"],
                            "available": pr["available"],
                        })
        return results[:20]

    def find_office_by_need(self, query: str) -> list[dict]:
        q = query.lower()
        results = []
        for p in self._places_of_type("department"):
            if q in p["name"].lower() or q in p["description"].lower():
                results.append({
                    "id": p["id"],
                    "name": p["name"],
                    "description": p["description"],
                    "department_type": "académico",
                    "purpose": "Docencia e investigación",
                    "services": ["información", "orientación"],
                })
        return results[:20]

    def get_gates(self) -> list[dict]:
        gates = []
        for p in self._places_of_type("gate"):
            gates.append({
                "id": p["id"],
                "name": p["name"],
                "description": p["description"],
                "gate_type": "principal",
                "entry_allowed": True,
                "exit_allowed": True,
                "adjacent_streets": ["Av. Universidad", "Calle Principal"],
            })
        return gates

    def search_semantic_documents(self, query: str) -> list[dict]:
        q = query.lower()
        docs = [
            {"entity_type": "regulation", "title": "Reglamento de Biblioteca",
             "content": "Horario de 7:00 a 23:00. Préstamo máximo 15 días."},
            {"entity_type": "guide", "title": "Guía de Laboratorios",
             "content": "Los laboratorios abren de 8:00 a 18:00. Reserva con 24h de anticipación."},
        ]
        results = []
        for d in docs:
            if q in d["title"].lower() or q in d["content"].lower():
                results.append({
                    "entity_type": d["entity_type"],
                    "title": d["title"],
                    "content": d["content"],
                })
        return results[:20]

    def get_current_crowd_levels(self) -> list[dict]:
        levels = []
        for p in self._places:
            levels.append({
                "place_id": p["id"],
                "place_name": p["name"],
                "level": "moderate",
                "percentage": 45.0,
                "source": "mock",
            })
        return levels

    def __del__(self):
        pass