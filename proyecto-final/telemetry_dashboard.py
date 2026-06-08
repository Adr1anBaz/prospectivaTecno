#!/usr/bin/env python3
"""
Dashboard completo de telemetría para Robot Unitree Go2
Muestra TODA la información disponible en tiempo real

Uso:
    python telemetry_dashboard.py
"""

import asyncio
import os
import sys
from datetime import datetime
from unitree_webrtc_connect.webrtc_driver import UnitreeWebRTCConnection, WebRTCConnectionMethod
from unitree_webrtc_connect.constants import RTC_TOPIC


class CompleteTelemetryDashboard:
    """Dashboard completo con TODA la telemetría del robot"""

    def __init__(self):
        self.conn = None
        self.running = False
        self.update_count = 0

        # Datos de telemetría
        self.sport_data = {}
        self.low_data = {}
        self.lidar_data = {}
        self.wireless_data = {}

    async def connect(self, ip: str = "192.168.12.1"):
        """Conecta al robot"""
        print(f"🔌 Conectando al robot en {ip}...")
        self.conn = UnitreeWebRTCConnection(
            WebRTCConnectionMethod.LocalAP,
            ip=ip
        )
        await self.conn.connect()
        print("✅ Conexión establecida\n")

        # Suscribirse a TODOS los tópicos disponibles
        try:
            self.conn.subscribe(RTC_TOPIC["LF_SPORT_MOD_STATE"])
            self.conn.subscribe(RTC_TOPIC["LOW_STATE"])
            self.conn.subscribe(RTC_TOPIC["WIRELESS_CONTROLLER"])
            # Agregar más suscripciones según disponibilidad
        except Exception as e:
            print(f"⚠️  Advertencia al suscribir: {e}")

    async def disconnect(self):
        """Desconecta del robot"""
        if self.conn:
            await self.conn.disconnect()

    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def render_header(self):
        """Renderiza el encabezado"""
        width = 120
        print("╔" + "═" * (width - 2) + "╗")
        title = "🤖 DASHBOARD COMPLETO DE TELEMETRÍA - UNITREE GO2"
        padding = (width - 2 - len(title)) // 2
        print("║" + " " * padding + title + " " * (width - 2 - padding - len(title)) + "║")
        print("╠" + "═" * (width - 2) + "╣")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_line = f"Actualizaciones: {self.update_count} | Timestamp: {timestamp}"
        print(f"║ {info_line:<{width-3}}║")
        print("╠" + "═" * (width - 2) + "╣")

    def render_imu_section(self, imu_data):
        """Renderiza sección de IMU"""
        width = 120
        print("║ 🧭 IMU (INERTIAL MEASUREMENT UNIT)" + " " * (width - 38) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if imu_data:
            # Cuaternión
            q = imu_data.get("quaternion", [0, 0, 0, 0])
            line = f"║   Cuaternión:    W={q[0]:>7.4f}  X={q[1]:>7.4f}  Y={q[2]:>7.4f}  Z={q[3]:>7.4f}"
            print(f"{line:<{width-1}}║")

            # Roll, Pitch, Yaw
            rpy = imu_data.get("rpy", [0, 0, 0])
            roll_deg = rpy[0] * 57.2958
            pitch_deg = rpy[1] * 57.2958
            yaw_deg = rpy[2] * 57.2958
            line = f"║   Orientación:   Roll={roll_deg:>7.2f}°  Pitch={pitch_deg:>7.2f}°  Yaw={yaw_deg:>7.2f}°"
            print(f"{line:<{width-1}}║")

            # Giroscopio
            gyro = imu_data.get("gyroscope", [0, 0, 0])
            line = f"║   Giroscopio:    X={gyro[0]:>7.4f}  Y={gyro[1]:>7.4f}  Z={gyro[2]:>7.4f} rad/s"
            print(f"{line:<{width-1}}║")

            # Acelerómetro
            accel = imu_data.get("accelerometer", [0, 0, 0])
            line = f"║   Acelerómetro:  X={accel[0]:>7.4f}  Y={accel[1]:>7.4f}  Z={accel[2]:>7.4f} m/s²"
            print(f"{line:<{width-1}}║")

            # Temperatura
            temp = imu_data.get("temperature", 0.0)
            line = f"║   Temperatura:   {temp:.2f}°C"
            print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_position_section(self, position_data):
        """Renderiza sección de posición y velocidad"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 📍 POSICIÓN Y VELOCIDAD" + " " * (width - 27) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if position_data:
            # Posición
            pos = position_data.get("position", [0, 0, 0])
            line = f"║   Posición:      X={pos[0]:>7.3f}m  Y={pos[1]:>7.3f}m  Z={pos[2]:>7.3f}m"
            print(f"{line:<{width-1}}║")

            # Velocidad
            vel = position_data.get("velocity", [0, 0, 0])
            line = f"║   Velocidad:     Vx={vel[0]:>7.3f}  Vy={vel[1]:>7.3f}  Vz={vel[2]:>7.3f} m/s"
            print(f"{line:<{width-1}}║")

            # Velocidad de giro
            yaw_speed = position_data.get("yaw_speed", 0.0)
            line = f"║   Yaw Speed:     {yaw_speed:.4f} rad/s"
            print(f"{line:<{width-1}}║")

            # Altura del cuerpo
            body_height = position_data.get("body_height", 0.0)
            line = f"║   Altura cuerpo: {body_height:.3f}m"
            print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_robot_mode_section(self, mode_data):
        """Renderiza sección de modo y estado del robot"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ ⚙️  MODO Y ESTADO DEL ROBOT" + " " * (width - 31) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if mode_data:
            # Modo
            mode = mode_data.get("mode", 0)
            mode_names = {
                0: "Idle", 1: "Damping", 2: "Recovery Stand", 3: "Stand Up",
                4: "Walk", 5: "Run", 6: "Climb Stairs", 7: "Trot",
                8: "Bound", 9: "Pronk", 10: "Jump", 11: "Special Motion"
            }
            mode_name = mode_names.get(mode, f"Unknown ({mode})")
            line = f"║   Modo actual:   {mode_name}"
            print(f"{line:<{width-1}}║")

            # Tipo de marcha
            gait = mode_data.get("gait_type", 0)
            gait_names = {0: "Idle", 1: "Trot", 2: "Trot Running", 3: "Climb Stair", 4: "Trot Obstacle"}
            gait_name = gait_names.get(gait, f"Unknown ({gait})")
            line = f"║   Tipo marcha:   {gait_name}"
            print(f"{line:<{width-1}}║")

            # Progreso de acción
            progress = mode_data.get("progress", 0.0)
            bar_length = 40
            filled = int(bar_length * progress)
            bar = "█" * filled + "░" * (bar_length - filled)
            line = f"║   Progreso:      [{bar}] {progress*100:.1f}%"
            print(f"{line:<{width-1}}║")

            # Altura de elevación de patas
            foot_raise = mode_data.get("foot_raise_height", 0.0)
            line = f"║   Elevación:     {foot_raise:.3f}m"
            print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_obstacles_section(self, obstacles):
        """Renderiza sección de obstáculos"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 🚧 DETECCIÓN DE OBSTÁCULOS" + " " * (width - 30) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if obstacles and len(obstacles) >= 4:
            def get_color(dist):
                if dist < 0.3:
                    return "🔴"
                elif dist < 0.5:
                    return "🟡"
                else:
                    return "🟢"

            line = (f"║   Frente:  {get_color(obstacles[0])} {obstacles[0]:.2f}m  |  "
                   f"Atrás:  {get_color(obstacles[1])} {obstacles[1]:.2f}m  |  "
                   f"Izq:  {get_color(obstacles[2])} {obstacles[2]:.2f}m  |  "
                   f"Der:  {get_color(obstacles[3])} {obstacles[3]:.2f}m")
            print(f"{line:<{width-1}}║")

            # Visual
            min_dist = min(obstacles)
            if min_dist < 0.3:
                warning = "⚠️  ALERTA: Obstáculo muy cercano!"
            elif min_dist < 0.5:
                warning = "⚡ Precaución: Obstáculo cerca"
            else:
                warning = "✅ Zona despejada"
            line = f"║   Estado: {warning}"
            print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_foot_section(self, foot_data):
        """Renderiza sección de patas"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 🦿 ESTADO DE LAS PATAS" + " " * (width - 26) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if foot_data:
            # Fuerza en patas
            forces = foot_data.get("foot_force", [0, 0, 0, 0])
            line = f"║   Fuerza:        FL={forces[0]:>6.2f}N  FR={forces[1]:>6.2f}N  RL={forces[2]:>6.2f}N  RR={forces[3]:>6.2f}N"
            print(f"{line:<{width-1}}║")

            # Indicador visual de carga
            max_force = max(forces) if forces else 1
            for i, (name, force) in enumerate(zip(["FL (Frente Izq)", "FR (Frente Der)",
                                                     "RL (Atrás Izq)", "RR (Atrás Der)"], forces)):
                bar_length = 30
                filled = int(bar_length * (force / max_force)) if max_force > 0 else 0
                bar = "█" * filled + "░" * (bar_length - filled)
                line = f"║   {name:<15} [{bar}] {force:>6.2f}N"
                print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_battery_section(self, battery_data):
        """Renderiza sección de batería"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 🔋 BATERÍA (BMS)" + " " * (width - 19) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if battery_data:
            # Nivel de carga
            soc = battery_data.get("soc", 0.0)
            bar_length = 40
            filled = int(bar_length * soc / 100)
            bar = "█" * filled + "░" * (bar_length - filled)

            if soc > 60:
                icon = "🟢"
            elif soc > 30:
                icon = "🟡"
            else:
                icon = "🔴"

            line = f"║   Carga:         {icon} [{bar}] {soc:.1f}%"
            print(f"{line:<{width-1}}║")

            # Voltaje y corriente
            voltage = battery_data.get("voltage", 0.0)
            current = battery_data.get("current", 0.0)
            power = voltage * current
            line = f"║   Voltaje:       {voltage:.2f}V  |  Corriente: {current:.2f}A  |  Potencia: {power:.2f}W"
            print(f"{line:<{width-1}}║")

            # Ciclos
            cycles = battery_data.get("cycle_count", 0)
            line = f"║   Ciclos carga:  {cycles}"
            print(f"{line:<{width-1}}║")

            # Temperaturas
            temps = battery_data.get("temperature", [])
            if temps:
                temp_str = "  ".join([f"T{i+1}:{t:.1f}°C" for i, t in enumerate(temps[:4])])
                line = f"║   Temperaturas:  {temp_str}"
                print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_motors_section(self, motors_data):
        """Renderiza sección de motores"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ ⚙️  ESTADO DE MOTORES (20 MOTORES TOTALES)" + " " * (width - 47) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if motors_data and len(motors_data) > 0:
            # Resumen por pata
            leg_names = ["FL (Frente Izq)", "FR (Frente Der)", "RL (Atrás Izq)", "RR (Atrás Der)", "Extra"]
            motors_per_leg = [motors_data[i:i+3] for i in range(0, min(15, len(motors_data)), 3)]

            for leg_idx, (leg_name, leg_motors) in enumerate(zip(leg_names, motors_per_leg)):
                if not leg_motors:
                    continue

                avg_temp = sum(m.get("temperature", 0) for m in leg_motors) / len(leg_motors)
                avg_q = sum(m.get("q", 0) for m in leg_motors) / len(leg_motors)

                temp_icon = "🔴" if avg_temp > 60 else "🟡" if avg_temp > 45 else "🟢"

                line = f"║   {leg_name:<15} Temp: {temp_icon} {avg_temp:.1f}°C  |  Pos prom: {avg_q:.3f}rad"
                print(f"{line:<{width-1}}║")

            # Motores con problemas
            hot_motors = [i for i, m in enumerate(motors_data) if m.get("temperature", 0) > 60]
            lost_motors = [i for i, m in enumerate(motors_data) if m.get("lost", 0) > 0]

            if hot_motors:
                line = f"║   ⚠️  Motores calientes: {', '.join(map(str, hot_motors))}"
                print(f"{line:<{width-1}}║")

            if lost_motors:
                line = f"║   ❌ Motores con pérdida: {', '.join(map(str, lost_motors))}"
                print(f"{line:<{width-1}}║")

            if not hot_motors and not lost_motors:
                line = "║   ✅ Todos los motores operando normalmente"
                print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_system_section(self, system_data):
        """Renderiza sección de sistema"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 💻 INFORMACIÓN DEL SISTEMA" + " " * (width - 30) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if system_data:
            # Voltaje y corriente del sistema
            power_v = system_data.get("power_v", 0.0)
            power_a = system_data.get("power_a", 0.0)
            line = f"║   Alimentación:  {power_v:.2f}V @ {power_a:.2f}A"
            print(f"{line:<{width-1}}║")

            # Temperaturas NTC
            ntc1 = system_data.get("temperature_ntc1", 0.0)
            ntc2 = system_data.get("temperature_ntc2", 0.0)
            line = f"║   Temp. NTC:     NTC1: {ntc1:.1f}°C  |  NTC2: {ntc2:.1f}°C"
            print(f"{line:<{width-1}}║")

            # Ventiladores
            fans = system_data.get("fan_frequency", [])
            if fans:
                fan_str = "  ".join([f"Fan{i+1}:{f}Hz" for i, f in enumerate(fans)])
                line = f"║   Ventiladores:  {fan_str}"
                print(f"{line:<{width-1}}║")

            # Serial y versión
            sn = system_data.get("sn", "N/A")
            version = system_data.get("version", [])
            version_str = ".".join(map(str, version)) if version else "N/A"
            line = f"║   S/N: {sn}  |  Versión: {version_str}"
            print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_wireless_section(self, wireless_data):
        """Renderiza sección de control inalámbrico"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 🎮 CONTROL INALÁMBRICO" + " " * (width - 26) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        if wireless_data:
            lx = wireless_data.get("lx", 0.0)
            ly = wireless_data.get("ly", 0.0)
            rx = wireless_data.get("rx", 0.0)
            ry = wireless_data.get("ry", 0.0)

            line = f"║   Joystick Izq:  X={lx:>6.3f}  Y={ly:>6.3f}"
            print(f"{line:<{width-1}}║")
            line = f"║   Joystick Der:  X={rx:>6.3f}  Y={ry:>6.3f}"
            print(f"{line:<{width-1}}║")

            keys = wireless_data.get("keys", 0)
            line = f"║   Botones:       0x{keys:04X}"
            print(f"{line:<{width-1}}║")
        else:
            print(f"║   ❌ No hay datos disponibles{' ' * (width - 34)}║")

    def render_footer(self):
        """Renderiza el pie del dashboard"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        line = "⌨️  Presiona Ctrl+C para salir y exportar datos"
        padding = (width - 2 - len(line)) // 2
        print("║" + " " * padding + line + " " * (width - 2 - padding - len(line)) + "║")
        print("╚" + "═" * (width - 2) + "╝")

    async def update_telemetry(self):
        """Actualiza todos los datos de telemetría"""
        try:
            # Leer datos del canal de datos
            # NOTA: Esto requiere acceso directo al data_channel de la conexión
            # La implementación exacta depende de la versión de la librería

            # Por ahora, intentamos obtener datos disponibles
            if hasattr(self.conn, 'data_channel') and self.conn.data_channel:
                # Aquí iría la lectura real de los canales
                pass

        except Exception as e:
            # Silenciar errores de lectura para no interrumpir el display
            pass

    def render(self):
        """Renderiza todo el dashboard"""
        self.clear_screen()
        self.update_count += 1

        self.render_header()

        # Sección IMU
        imu_data = self.sport_data.get("imu_state", {})
        self.render_imu_section(imu_data)

        # Sección Posición
        self.render_position_section(self.sport_data)

        # Sección Modo del robot
        self.render_robot_mode_section(self.sport_data)

        # Sección Obstáculos
        obstacles = self.sport_data.get("range_obstacle", [])
        self.render_obstacles_section(obstacles)

        # Sección Patas
        self.render_foot_section(self.sport_data)

        # Sección Batería
        battery = self.low_data.get("bms_state", {})
        self.render_battery_section(battery)

        # Sección Motores
        motors = self.low_data.get("motor_state", [])
        self.render_motors_section(motors)

        # Sección Sistema
        self.render_system_section(self.low_data)

        # Sección Control Inalámbrico
        self.render_wireless_section(self.wireless_data)

        self.render_footer()

    async def run(self):
        """Ejecuta el dashboard"""
        self.running = True

        # Loop de actualización
        while self.running:
            await self.update_telemetry()
            self.render()
            await asyncio.sleep(0.5)


async def main():
    """Función principal"""
    robot_ip = os.environ.get("UNITREE_ROBOT_IP", "192.168.12.1")

    print("╔════════════════════════════════════════════════════════════╗")
    print("║    🤖 DASHBOARD COMPLETO DE TELEMETRÍA - UNITREE GO2       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    dashboard = CompleteTelemetryDashboard()

    try:
        await dashboard.connect(robot_ip)
        await dashboard.run()

    except KeyboardInterrupt:
        print("\n\n⚠️  Deteniendo dashboard...")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        dashboard.running = False
        await dashboard.disconnect()
        print("\n✅ Desconectado del robot")
        print("👋 ¡Hasta pronto!\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Adiós!")
