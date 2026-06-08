#!/usr/bin/env python3
"""
Script de diagnóstico para probar conexión al robot Unitree
Prueba diferentes métodos y IPs
"""

import asyncio
import os
from unitree_webrtc_connect.webrtc_driver import UnitreeWebRTCConnection, WebRTCConnectionMethod

# Configuraciones a probar
CONFIGS = [
    {"method": WebRTCConnectionMethod.LocalAP, "ip": "192.168.12.1", "name": "LocalAP (Default)"},
    {"method": WebRTCConnectionMethod.LocalSTA, "ip": "192.168.12.1", "name": "LocalSTA"},
    {"method": WebRTCConnectionMethod.LocalAP, "ip": "192.168.123.161", "name": "LocalAP (Alt IP 1)"},
    {"method": WebRTCConnectionMethod.LocalAP, "ip": "192.168.123.15", "name": "LocalAP (Alt IP 2)"},
]

async def test_connection(config):
    """Prueba una configuración específica"""
    print(f"\n{'='*60}")
    print(f"🔍 Probando: {config['name']}")
    print(f"{'='*60}")
    print(f"   Método: {config['method']}")
    print(f"   IP: {config['ip']}")

    try:
        conn = UnitreeWebRTCConnection(
            config['method'],
            ip=config['ip']
        )

        print(f"   Intentando conectar...")
        await conn.connect()

        print(f"\n✅ ¡ÉXITO! Conexión establecida")
        print(f"   Esta configuración funciona:")
        print(f"   - Método: {config['method']}")
        print(f"   - IP: {config['ip']}")

        # Mantener conexión 2 segundos
        await asyncio.sleep(2)

        # Desconectar
        await conn.disconnect()
        print(f"   Desconectado correctamente")

        return True

    except Exception as e:
        print(f"   ❌ Falló: {e}")
        return False

async def main():
    """Prueba todas las configuraciones"""
    print("="*60)
    print("🤖 DIAGNÓSTICO DE CONEXIÓN UNITREE")
    print("="*60)
    print("\nProbando diferentes configuraciones...")

    success_count = 0

    for config in CONFIGS:
        result = await test_connection(config)
        if result:
            success_count += 1
            print(f"\n🎉 Configuración exitosa encontrada!")
            print(f"   Usa esta configuración en robot_voice_controller.py")
            break

        # Pequeña pausa entre intentos
        await asyncio.sleep(1)

    print(f"\n{'='*60}")
    print(f"📊 RESUMEN")
    print(f"{'='*60}")

    if success_count > 0:
        print(f"✅ Se encontró {success_count} configuración(es) funcional(es)")
    else:
        print(f"❌ Ninguna configuración funcionó")
        print(f"\n🔧 POSIBLES PROBLEMAS:")
        print(f"   1. El robot no está completamente iniciado")
        print(f"      → Espera 30-60 segundos después del pitido")
        print(f"   2. El robot necesita estar en modo WebRTC")
        print(f"      → Usa la app oficial de Unitree primero")
        print(f"   3. Firewall del robot activo")
        print(f"      → Verifica configuración del robot")
        print(f"   4. Versión de firmware incompatible")
        print(f"      → Actualiza el firmware del robot")
        print(f"   5. Modelo de robot no compatible")
        print(f"      → Verifica que sea Go2 con soporte WebRTC")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida")
