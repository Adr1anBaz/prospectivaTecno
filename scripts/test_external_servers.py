#!/usr/bin/env python3
"""
Test rapido de conexion entre el asistente y los servidores externos:
- MCP server (mcp-blu)
- Route server (mcp-blu route_server.py)

No requiere API keys de Groq/Deepgram; solo verifica que los clientes
puedan conectarse y llamar herramientas reales.

Uso:
    uv run python scripts/test_external_servers.py

Requiere que esten corriendo:
    cd mcp-blu/mcp-server && uv run server.py
    cd mcp-blu && uv run route_server.py
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv

load_dotenv()

from prospectiva.utils.mcp_client import MCPClient
from prospectiva.utils.route_client import RouteClient


def test_mcp():
    print("\n" + "=" * 60)
    print("TEST MCP Server")
    print("=" * 60)

    url = os.getenv("MCP_URL", "http://localhost:8000/mcp")
    token = os.getenv("MCP_BEARER_TOKEN", "")

    print(f"Conectando a {url} ...")
    client = MCPClient(url=url, token=token)

    if not client.is_available():
        print("ERROR: No se pudo conectar al MCP server")
        return False

    print("OK: Conectado al MCP server")

    health = client.health_check()
    print(f"health_check: {health}")

    summary = client.database_summary()
    print(f"database_summary: {summary}")

    places = client.search_places("Giornale")
    print(f"search_places('Giornale'): {len(places)} resultado(s)")
    if places:
        print(f"  - {places[0].get('name')} ({places[0].get('type')})")

    return True


def test_route():
    print("\n" + "=" * 60)
    print("TEST Route Server")
    print("=" * 60)

    url = os.getenv("ROUTE_API_URL", "http://localhost:8001")
    token = os.getenv("MCP_BEARER_TOKEN", "")

    print(f"Conectando a {url} ...")
    client = RouteClient(base_url=url, token=token)

    if not client.is_available():
        print("ERROR: No se pudo conectar al Route server")
        return False

    print("OK: Conectado al Route server")

    result = client.calculate_route("Laboratorio L", "Giornale")
    print(f"calculate_route: {result}")

    return result.get("success", False)


if __name__ == "__main__":
    ok_mcp = test_mcp()
    ok_route = test_route()

    print("\n" + "=" * 60)
    if ok_mcp and ok_route:
        print("OK: Ambos servidores responden correctamente")
    else:
        print("ERROR: Al menos un servidor fallo")
        print(f"  MCP:   {'OK' if ok_mcp else 'FAIL'}")
        print(f"  Route: {'OK' if ok_route else 'FAIL'}")
    print("=" * 60)
