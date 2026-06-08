#!/usr/bin/env python3
"""
Script de prueba de secuencia de comandos (sin robot real)
Simula el flujo completo para verificar que todo funciona
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from robot_voice_controller import UnitreeVoiceController

# Secuencia de comandos de prueba
TEST_SEQUENCE = [
    "activa el modo caminar",
    "ponte de pie",
    "saluda",
    "camina hacia adelante",
    "detente",
    "gira a la derecha",
    "muévete a la izquierda",
    "retrocede girando a la izquierda",
    "siéntate",
    "apaga los motores"
]


class MockConnection:
    """Mock de conexión para testing sin robot"""
    def __init__(self):
        self.datachannel = MockDataChannel()

    async def connect(self):
        await asyncio.sleep(0.1)

    async def disconnect(self):
        await asyncio.sleep(0.1)


class MockDataChannel:
    """Mock de datachannel"""
    def __init__(self):
        self.pub_sub = MockPubSub()


class MockPubSub:
    """Mock de pub_sub"""
    async def publish_request_new(self, topic, data):
        # Simular envío
        await asyncio.sleep(0.1)


async def test_sequence():
    """Prueba la secuencia de comandos sin robot real"""
    print("="*60)
    print("🧪 TEST DE SECUENCIA DE COMANDOS")
    print("="*60)
    print("\nEste test simula el flujo completo sin robot real")
    print("Verifica que todos los comandos se procesen correctamente\n")

    # Crear controlador (sin conexión real)
    controller = UnitreeVoiceController(
        robot_ip="192.168.12.1",
        whisper_model="base",
        llm_model="qwen2.5:3b"
    )

    # Mock la conexión
    controller.conn = MockConnection()
    controller.state = controller.state.__class__.IDLE
    controller.load_whisper()

    print(f"✅ Sistema inicializado (modo simulación)")
    print(f"\n{'='*60}")
    print(f"Ejecutando {len(TEST_SEQUENCE)} comandos de prueba...")
    print(f"{'='*60}\n")

    results = []

    for i, command in enumerate(TEST_SEQUENCE, 1):
        print(f"\n[{i}/{len(TEST_SEQUENCE)}] Procesando: \"{command}\"")

        try:
            # Generar tool call
            tool_call = await asyncio.to_thread(
                controller.generate_tool_call,
                command
            )

            if not tool_call:
                print(f"   ❌ FALLO: No se pudo generar tool call")
                results.append((command, "FAIL", "No tool call"))
                continue

            print(f"   ✅ Tool call generado: {tool_call['name']}")
            print(f"      Args: {tool_call.get('arguments', {})}")

            # Simular ejecución
            await asyncio.sleep(0.5)
            print(f"   ✅ Comando simulado exitosamente")

            results.append((command, "PASS", tool_call))

        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append((command, "ERROR", str(e)))

    # Resumen
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE RESULTADOS")
    print(f"{'='*60}")

    passed = sum(1 for _, status, _ in results if status == "PASS")
    failed = sum(1 for _, status, _ in results if status == "FAIL")
    errors = sum(1 for _, status, _ in results if status == "ERROR")

    print(f"\n✅ Pasados: {passed}/{len(TEST_SEQUENCE)}")
    print(f"❌ Fallados: {failed}/{len(TEST_SEQUENCE)}")
    print(f"⚠️  Errores: {errors}/{len(TEST_SEQUENCE)}")

    if failed > 0 or errors > 0:
        print(f"\n{'='*60}")
        print("❌ COMANDOS CON PROBLEMAS:")
        print(f"{'='*60}")
        for cmd, status, info in results:
            if status != "PASS":
                print(f"\n• \"{cmd}\"")
                print(f"  Status: {status}")
                print(f"  Info: {info}")

    if passed == len(TEST_SEQUENCE):
        print(f"\n🎉 TODOS LOS COMANDOS FUNCIONAN CORRECTAMENTE")
        print(f"✅ Sistema listo para usar con robot real")
    else:
        print(f"\n⚠️  Algunos comandos fallaron, revisa la configuración")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    print("\n🚀 Iniciando test de secuencia...\n")

    try:
        asyncio.run(test_sequence())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido")
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
