#!/usr/bin/env python3
"""
Test script para probar el sistema SIN los servicios de otros equipos.

Usa:
- MockMCPClient (datos ficticios de la universidad)
- MockRouteClient (rutas ficticias entre nodos)
- Groq LLM con tool calling nativo

Muestra:
- Qué herramientas llama el LLM automáticamente
- El flujo completo de conversación multi-turno
- Cálculo de ruta y envío de secuencia de movimiento

Ejecutar:
    uv run python tests/test_tool_calling.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from prospectiva.modulos.llm.groq_llm import GroqLLM
from prospectiva.utils.mock_mcp_client import MockMCPClient
from prospectiva.utils.mock_route_client import MockRouteClient
from prospectiva.utils.memory import ConversationMemory
from prospectiva.utils.tool_tracker import ToolUsageTracker
from prospectiva.procesos.actions.navigation_actions import NavigationActions


def test_tool_calling():
    """Test LLM tool calling with mock data."""
    print("=" * 70)
    print("🧪 TEST: Tool Calling Nativo con Groq llama-3.1-8b-instant")
    print("=" * 70)
    
    # Setup
    llm = GroqLLM()
    mcp = MockMCPClient()
    route = MockRouteClient()
    memory = ConversationMemory()
    tracker = ToolUsageTracker()
    
    print("\n✅ Mock MCP: Datos de universidad cargados")
    print(f"   Nodos: {len(mcp.get_nodes())}")
    print(f"   Lugares: {len(mcp._mock_data['places'])}")
    print(f"   Categorías: {mcp.get_categories()}")
    
    print("\n✅ Mock Route: Rutas predefinidas cargadas")
    print(f"   Rutas: {len(route._mock_routes)}")
    
    # Test 1: Direct question that triggers search
    print("\n" + "=" * 70)
    print("TEST 1: Usuario pregunta 'quiero comer'")
    print("=" * 70)
    
    user_query = "quiero comer"
    memory.add_turn("user", user_query)
    
    # Define tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_places",
                "description": "Search for places in the university",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "category": {"type": "string"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_node_info",
                "description": "Get info about a node",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "node_name": {"type": "string"}
                    },
                    "required": ["node_name"]
                }
            }
        }
    ]
    
    # System prompt
    system_prompt = f"""Eres un asistente de navegación universitario. Hablas español.
    
REGLAS:
- Si el usuario pide un lugar específico, infiere el destino
- Si es vago, haz preguntas de seguimiento
- Máximo 2 preguntas
- Máximo 1 oración en tu respuesta
- Tu posición actual: {memory.get_current_node()}
"""
    
    print(f"\n📝 User: {user_query}")
    print("🤖 LLM procesando (con tool calling)...")
    
    # Call LLM with tools
    response = llm.generate_with_tools(
        prompt=user_query,
        tools=tools,
        system_prompt=system_prompt
    )
    
    print(f"\n📊 LLM Response:")
    print(f"   finish_reason: {response['finish_reason']}")
    print(f"   content: {response['content']}")
    print(f"   tool_calls: {len(response['tool_calls'])}")
    
    # Execute tools if any
    if response['tool_calls']:
        print("\n🔧 Herramientas llamadas por el LLM:")
        for i, tc in enumerate(response['tool_calls'], 1):
            print(f"   {i}. {tc['name']}(" + ", ".join([f"{k}={v}" for k, v in tc['arguments'].items()]) + ")")
            
            # Execute tool
            start = time.time()
            if tc['name'] == 'search_places':
                result = mcp.search(**tc['arguments'])
            elif tc['name'] == 'get_node_info':
                result = mcp.get_node(**tc['arguments'])
            else:
                result = {"error": "Unknown tool"}
            
            duration = (time.time() - start) * 1000
            tracker.record(tc['name'], tc['arguments'], result, duration)
            print(f"      Result: {len(result) if isinstance(result, list) else result} ({duration:.0f}ms)")
        
        # Send tool results back to LLM
        print("\n📤 Enviando resultados de herramientas al LLM...")
        tool_results = []
        for tc in response['tool_calls']:
            if tc['name'] == 'search_places':
                result = mcp.search(**tc['arguments'])
            elif tc['name'] == 'get_node_info':
                result = mcp.get_node(**tc['arguments'])
            else:
                result = {"error": "Unknown tool"}
            
            tool_results.append({
                "tool_call_id": tc['id'],
                "result": result
            })
        
        final_response = llm.send_tool_results(
            tool_calls=response['tool_calls'],
            tool_results=tool_results,
            system_prompt=system_prompt
        )
        
        print(f"\n📥 Respuesta final del LLM:")
        print(f"   Content: {final_response['content']}")
        
        # Track in memory
        memory.add_turn("assistant", final_response['content'])
    else:
        memory.add_turn("assistant", response['content'])
    
    # Print tool usage summary
    print(tracker.get_summary())
    
    # Test 2: Navigation
    print("\n" + "=" * 70)
    print("TEST 2: Simular navegación con Route API")
    print("=" * 70)
    
    current_node = memory.get_current_node()
    end_node = "giornale"
    
    print(f"\n🗺️ Calculando ruta: {current_node} → {end_node}")
    route_result = route.calculate_route(current_node, end_node)
    
    if route_result['success']:
        print(f"✅ Ruta calculada:")
        print(f"   Archivos: {route_result['movement_files']}")
        print(f"   Path: {route_result['path']}")
        print(f"   Tiempo: {route_result['estimated_time']}s")
        
        # Update position
        memory.set_current_node(end_node)
        print(f"📍 Posición actualizada: {end_node}")
    
    # Test 3: NavigationActions
    print("\n" + "=" * 70)
    print("TEST 3: NavigationActions con Route API")
    print("=" * 70)
    
    nav = NavigationActions(route)
    result = nav.navigate({
        'text': 'llévame a biomédica',
        'destination': 'BIOMEDICA',
        'current_node': 'pasillo_a'
    })
    
    print(f"\n✅ Resultado:")
    print(f"   Status: {result['status']}")
    print(f"   Node: {result.get('node')}")
    print(f"   Name: {result.get('name')}")
    print(f"   Files: {result.get('movement_files')}")
    print(f"   Path: {result.get('path')}")
    
    print("\n" + "=" * 70)
    print("✅ TESTS COMPLETADOS")
    print("=" * 70)
    print(f"\n📊 Resumen:")
    print(f"   Herramientas usadas: {tracker.count()}")
    print(f"   Nombres: {tracker.get_tool_names()}")
    print(f"   Nodo final: {memory.get_current_node()}")
    print(f"   Historial: {len(memory.get_history())} turnos")


def test_mock_data():
    """Test mock data directly."""
    print("\n" + "=" * 70)
    print("🧪 TEST: Datos Mock de la Universidad")
    print("=" * 70)
    
    mcp = MockMCPClient()
    
    print("\n📍 Nodos disponibles:")
    for node in mcp.get_nodes()[:10]:
        print(f"   - {node}")
    
    print("\n🔍 Buscando 'comida':")
    results = mcp.search("comida")
    for r in results:
        print(f"   - {r['name']} ({r['category']})")
    
    print("\n🔍 Buscando 'italiano':")
    results = mcp.search("italiano")
    for r in results:
        print(f"   - {r['name']}: {r['description']}")
    
    print("\n📋 Categorías:")
    for cat in mcp.get_categories():
        print(f"   - {cat}")
    
    print("\n📍 Info de nodo 'giornale':")
    node = mcp.get_node("giornale")
    if node:
        print(f"   Name: {node['name']}")
        print(f"   Connected: {node['connected']}")


if __name__ == "__main__":
    test_mock_data()
    test_tool_calling()
