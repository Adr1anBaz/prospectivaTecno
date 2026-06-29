#!/usr/bin/env python3
"""Test de verificacion: respuestas limpias, navegacion, busqueda de laboratorios."""
import sys, os, time
sys.path.insert(0, "src")
from dotenv import load_dotenv
load_dotenv()

from prospectiva.modulos.llm.fallback_llm import FallbackLLM
from prospectiva.modulos.llm.groq_llm import GroqLLM
from prospectiva.modulos.llm.openrouter_llm import OpenRouterLLM
from prospectiva.utils.mcp_client import MCPClient
from prospectiva.utils.route_client import RouteClient
from prospectiva.procesos.orquestador import Orquestador

mcp = MCPClient(); assert mcp.is_available(), "MCP no disponible"
rc = RouteClient(); assert rc.is_available(), "Route no disponible"

or_key = os.getenv("OPENROUTER_API_KEY", "")
llm = FallbackLLM(primary=GroqLLM(), secondary=OpenRouterLLM(api_key=or_key))

SYS = """Eres asistente universitario. Hablas espanol.

DATOS DISPONIBLES:
Restaurantes: Tacos Don Julio, Sushi Nagoya, Cafe Borrego, etc.
Laboratorios: Robotica (ROS), Circuitos (FPGA), Control (projector)
Equipamiento en INGLES: 'projector', 'ROS', 'FPGA', 'robots'

GUIA:
- NAVEGAR a un lugar -> navigate_to
- BUSCAR lugares -> search_places (prueba terminos simples o en ingles)
- COMIDA -> search_food
- PRODUCTOS -> search_products
- DETALLE de un lugar -> get_place_detail_by_name

REGLAS:
- USA LAS HERRAMIENTAS siempre
- Si no encuentras con un termino, prueba con sinonimos mas simples o en ingles
- NUNCA uses <function=...> ni <...> en tu respuesta
- Responde en 1 oracion natural"""

tools = Orquestador.LLM_TOOLS

queries = [
    "que laboratorio tiene proyector",
    "donde comprar calculadora",
    "llevame a cafe borrego",
    "que hay en el menu de sushi nagoya",
]

for q in queries:
    print(f"\n=== {q} ===")
    t0 = time.time()
    r = llm.generate_with_tools(q, tools, SYS)
    t1 = time.time()
    tc = r.get("tool_calls", [])
    if tc:
        name, args = tc[0]["name"], tc[0]["arguments"]
        dest = args.get("destination") or args.get("query") or args.get("name")
        print(f"  [{t1-t0:.2f}s] {name}({dest})")
        if name == "navigate_to":
            route = rc.calculate_route("Interseccion central del campus", dest)
            if route.get("success"):
                print(f"  Ruta: {' -> '.join(route['path'])}")
                print(f"  Dist: {route['total_distance_m']}m | T: {route['estimated_time']}s")
            else:
                print(f"  Ruta NO disponible: {route.get('error','?')}")
        elif name == "search_places":
            res = mcp._call_tool(name, args)
            print(f"  Resultados: {len(res) if isinstance(res, list) else '?'}")
    else:
        text = r.get("content", "") or ""
        has_syntax = "<function=" in text or "<" in text
        print(f"  [{t1-t0:.2f}s] {'❌ CONTIENE SINTAXIS' if has_syntax else '✅'} {text[:100]}")
