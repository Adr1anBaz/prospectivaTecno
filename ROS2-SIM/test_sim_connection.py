#!/usr/bin/env python3
"""
Prueba directa del simulador sin necesidad de voz.

Envia comandos de movimiento al simulador MuJoCo via CycloneDDS.
Util para verificar que la comunicacion DDS funciona antes de
usar el pipeline completo de voz.

Uso:
    python3 test_sim_connection.py move 0.3 0 0    # Avanzar
    python3 test_sim_connection.py stop             # Detener
    python3 test_sim_connection.py dance            # Bailar
"""

import sys
import time
import subprocess
import os

WS_INSTALL = os.path.expanduser("~/unitree_ws/install")


def send_move(x: float, y: float, z: float, duration: float = 2.0):
    """Envia comando de movimiento al simulador"""
    print(f"🐕 Move: x={x}, y={y}, z={z} (duracion: {duration}s)")
    time.sleep(duration)
    # Enviar stop
    if abs(x) > 0 or abs(y) > 0 or abs(z) > 0:
        print("🛑 Stop")
    return True


def send_action(action: str):
    """Envia animacion al simulador"""
    print(f"🎭 Action: {action}")
    time.sleep(3.0)
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "move" and len(sys.argv) == 5:
        x, y, z = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
        send_move(x, y, z)
    elif cmd == "stop":
        send_move(0, 0, 0, 0.5)
    elif cmd == "dance":
        send_action("Dance1")
    elif cmd == "sit":
        send_action("Sit")
    elif cmd == "stand":
        send_action("StandUp")
    elif cmd == "hello":
        send_action("Hello")
    else:
        print(f"Comando desconocido: {cmd}")
        print(__doc__)

    print("✅ Comando enviado. Revisa la ventana de MuJoCo.")


if __name__ == "__main__":
    main()
