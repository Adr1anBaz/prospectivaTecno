#!/usr/bin/env python3
"""
Demo de telemetría en tiempo real del Robot Unitree Go2
Muestra información actualizada en la terminal
"""

import asyncio
import os
from robot_telemetry import RobotTelemetry
from unitree_webrtc_connect.webrtc_driver import UnitreeWebRTCConnection, WebRTCConnectionMethod


class TelemetryDisplay:
    """Display en tiempo real de telemetría"""

    def __init__(self):
        self.update_count = 0

    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def format_orientation(self, orientation):
        """Formatea datos de orientación"""
        if not orientation:
            return "❌ No disponible"

        return (f"Roll: {orientation['roll']:>7.2f}° | "
                f"Pitch: {orientation['pitch']:>7.2f}° | "
                f"Yaw: {orientation['yaw']:>7.2f}°")

    def format_position(self, position):
        """Formatea datos de posición"""
        if not position:
            return "❌ No disponible"

        return (f"X: {position['x']:>6.3f}m | "
                f"Y: {position['y']:>6.3f}m | "
                f"Z: {position['z']:>6.3f}m")

    def format_battery(self, battery):
        """Formatea datos de batería"""
        if not battery:
            return "❌ No disponible"

        level = battery['level_percent']
        bar_length = 20
        filled = int(bar_length * level / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Color según nivel
        if level > 60:
            color = "🟢"
        elif level > 30:
            color = "🟡"
        else:
            color = "🔴"

        return (f"{color} [{bar}] {level:.1f}% | "
                f"{battery['voltage']:.1f}V | "
                f"{battery['current']:.2f}A")

    def format_obstacles(self, obstacles):
        """Formatea datos de obstáculos"""
        if not obstacles:
            return "❌ No disponible"

        def distance_indicator(dist):
            if dist < 0.3:
                return f"🔴 {dist:.2f}m"
            elif dist < 0.5:
                return f"🟡 {dist:.2f}m"
            else:
                return f"🟢 {dist:.2f}m"

        return (f"↑ {distance_indicator(obstacles['front'])} | "
                f"↓ {distance_indicator(obstacles['back'])} | "
                f"← {distance_indicator(obstacles['left'])} | "
                f"→ {distance_indicator(obstacles['right'])}")

    def display(self, telemetry: RobotTelemetry):
        """Muestra telemetría completa"""
        self.clear_screen()
        self.update_count += 1

        summary = telemetry.get_telemetry_summary()

        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "🤖 TELEMETRÍA ROBOT UNITREE GO2" + " " * 27 + "║")
        print("╠" + "═" * 78 + "╣")

        # Orientación
        print("║ 🧭 ORIENTACIÓN:" + " " * 63 + "║")
        orient_str = self.format_orientation(summary['orientation'])
        print(f"║    {orient_str:<74}║")
        print("╠" + "─" * 78 + "╣")

        # Posición
        print("║ 📍 POSICIÓN:" + " " * 65 + "║")
        pos_str = self.format_position(summary['position'])
        print(f"║    {pos_str:<74}║")
        print("╠" + "─" * 78 + "╣")

        # Batería
        print("║ 🔋 BATERÍA:" + " " * 66 + "║")
        bat_str = self.format_battery(summary['battery'])
        print(f"║    {bat_str:<74}║")
        print("╠" + "─" * 78 + "╣")

        # Obstáculos
        print("║ 🚧 OBSTÁCULOS:" + " " * 64 + "║")
        obs_str = self.format_obstacles(summary['obstacles'])
        print(f"║    {obs_str:<74}║")
        print("╠" + "═" * 78 + "╣")

        # Info
        print(f"║ 📊 Actualizaciones: {self.update_count:<10} | "
              f"Timestamp: {summary['timestamp']:<33}║")
        print("╠" + "═" * 78 + "╣")
        print("║ ⌨️  Presiona Ctrl+C para salir" + " " * 47 + "║")
        print("╚" + "═" * 78 + "╝")


async def main():
    """Demo principal"""
    robot_ip = os.environ.get("UNITREE_ROBOT_IP", "192.168.12.1")

    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "🤖 DEMO DE TELEMETRÍA" + " " * 33 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print(f"📡 Conectando al robot en {robot_ip}...")

    try:
        # Conectar al robot
        conn = UnitreeWebRTCConnection(
            WebRTCConnectionMethod.LocalAP,
            ip=robot_ip
        )
        await conn.connect()
        print("✅ Conectado exitosamente\n")
        await asyncio.sleep(1)

        # Crear gestor de telemetría
        telemetry = RobotTelemetry(conn)
        display = TelemetryDisplay()

        # Callbacks para alertas
        async def on_obstacle(distance, all_distances):
            """Alerta de obstáculo cercano"""
            # Esta función se puede usar para logging o acciones automáticas
            pass

        async def on_low_battery(state):
            """Alerta de batería baja"""
            if state.battery and state.battery.soc < 20:
                print("\n⚠️  ALERTA: Batería baja (<20%)\n")

        # Asignar callbacks
        telemetry.on_obstacle_detected = on_obstacle
        telemetry.on_low_update = on_low_battery

        # Iniciar monitoreo
        await telemetry.start_monitoring(
            sport_mode=True,
            low_level=True,
            update_rate=0.5
        )

        # Display loop
        while True:
            await asyncio.sleep(0.5)
            display.display(telemetry)

    except KeyboardInterrupt:
        print("\n\n⚠️  Deteniendo telemetría...")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        # Cleanup
        if 'telemetry' in locals():
            await telemetry.stop_monitoring()

            # Exportar datos finales
            print("\n💾 Exportando datos...")
            telemetry.export_to_json("telemetry_log.json")

        if 'conn' in locals():
            await conn.disconnect()

        print("✅ Desconectado del robot")
        print("\nGracias por usar la telemetría de Unitree Go2 🤖\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Adiós!")
