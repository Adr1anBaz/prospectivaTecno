#!/usr/bin/env python3
"""
Demo de telemetría con datos SIMULADOS
Útil para desarrollo y testing sin robot físico

Uso:
    python telemetry_demo.py
"""

import asyncio
import os
import random
import math
from datetime import datetime


class SimulatedTelemetryDashboard:
    """Dashboard con datos simulados realistas"""

    def __init__(self):
        self.running = False
        self.update_count = 0
        self.time = 0.0

        # Estado simulado
        self.mode = 4  # Walk mode
        self.gait = 1  # Trot
        self.battery_soc = 75.0
        self.position = [0.0, 0.0, 0.0]
        self.velocity = [0.0, 0.0, 0.0]

    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def generate_imu_data(self):
        """Genera datos simulados de IMU"""
        # Simular movimiento suave
        roll = 0.05 * math.sin(self.time * 0.5)
        pitch = 0.03 * math.sin(self.time * 0.7)
        yaw = self.time * 0.1

        return {
            "quaternion": [
                math.cos(yaw/2),
                roll * 0.1,
                pitch * 0.1,
                math.sin(yaw/2)
            ],
            "rpy": [roll, pitch, yaw],
            "gyroscope": [
                0.05 * math.sin(self.time),
                0.03 * math.cos(self.time * 1.2),
                0.02 * math.sin(self.time * 0.8)
            ],
            "accelerometer": [
                0.1 * math.sin(self.time * 2),
                0.08 * math.cos(self.time * 1.5),
                9.81 + 0.2 * math.sin(self.time)
            ],
            "temperature": 42.5 + random.uniform(-2, 2)
        }

    def generate_position_data(self):
        """Genera datos simulados de posición"""
        # Simular movimiento
        self.position[0] += 0.01 * math.sin(self.time * 0.5)
        self.position[1] += 0.005 * math.cos(self.time * 0.5)
        self.velocity = [
            0.5 * math.sin(self.time * 0.5),
            0.2 * math.cos(self.time * 0.5),
            0.0
        ]

        return {
            "position": self.position.copy(),
            "velocity": self.velocity,
            "yaw_speed": 0.1 * math.sin(self.time * 0.3),
            "body_height": 0.28 + 0.02 * math.sin(self.time * 2)
        }

    def generate_mode_data(self):
        """Genera datos de modo del robot"""
        return {
            "mode": self.mode,
            "gait_type": self.gait,
            "progress": (math.sin(self.time * 2) + 1) / 2,  # 0-1
            "foot_raise_height": 0.08 + 0.02 * math.sin(self.time * 3)
        }

    def generate_obstacles(self):
        """Genera distancias a obstáculos"""
        base_dist = 2.0
        return [
            base_dist + 0.5 * math.sin(self.time * 0.5),  # Front
            base_dist + 0.3 * math.cos(self.time * 0.6),  # Back
            base_dist + 0.4 * math.sin(self.time * 0.7),  # Left
            base_dist + 0.6 * math.cos(self.time * 0.4)   # Right
        ]

    def generate_foot_data(self):
        """Genera datos de patas"""
        # Simular carga alternada en patas (patrón de trote)
        phase = self.time * 3
        return {
            "foot_force": [
                100 + 50 * abs(math.sin(phase)),
                100 + 50 * abs(math.sin(phase + math.pi)),
                100 + 50 * abs(math.sin(phase + math.pi)),
                100 + 50 * abs(math.sin(phase))
            ]
        }

    def generate_battery_data(self):
        """Genera datos de batería"""
        # Simular descarga lenta
        self.battery_soc = max(20, self.battery_soc - 0.001)

        return {
            "soc": self.battery_soc,
            "voltage": 29.4 * (self.battery_soc / 100),
            "current": 2.5 + random.uniform(-0.5, 0.5),
            "cycle_count": 142,
            "temperature": [
                35.2 + random.uniform(-1, 1),
                34.8 + random.uniform(-1, 1),
                35.5 + random.uniform(-1, 1),
                35.0 + random.uniform(-1, 1)
            ]
        }

    def generate_motors_data(self):
        """Genera datos de 20 motores"""
        motors = []
        for i in range(20):
            leg_phase = (self.time * 3) + (i % 4) * (math.pi / 2)
            motors.append({
                "q": 0.5 * math.sin(leg_phase + i * 0.3),
                "dq": 0.3 * math.cos(leg_phase),
                "ddq": -0.5 * math.sin(leg_phase),
                "tau_est": 5.0 + 3.0 * abs(math.sin(leg_phase)),
                "temperature": 45 + random.uniform(-5, 10) + (i * 0.2),
                "lost": 0
            })
        return motors

    def generate_system_data(self):
        """Genera datos del sistema"""
        return {
            "power_v": 29.4 + random.uniform(-0.5, 0.5),
            "power_a": 3.2 + random.uniform(-0.3, 0.3),
            "temperature_ntc1": 48.5 + random.uniform(-2, 2),
            "temperature_ntc2": 47.2 + random.uniform(-2, 2),
            "fan_frequency": [
                int(3000 + random.uniform(-200, 200)),
                int(3100 + random.uniform(-200, 200))
            ],
            "sn": "GO2-DEMO-12345",
            "version": [1, 0, 32]
        }

    def generate_wireless_data(self):
        """Genera datos de control inalámbrico"""
        return {
            "lx": 0.3 * math.sin(self.time * 0.5),
            "ly": 0.2 * math.cos(self.time * 0.5),
            "rx": 0.0,
            "ry": 0.0,
            "keys": 0x0000
        }

    def render_header(self):
        """Renderiza el encabezado"""
        width = 120
        print("╔" + "═" * (width - 2) + "╗")
        title = "🤖 DASHBOARD DE TELEMETRÍA - MODO SIMULACIÓN"
        padding = (width - 2 - len(title)) // 2
        print("║" + " " * padding + title + " " * (width - 2 - padding - len(title)) + "║")
        print("╠" + "═" * (width - 2) + "╣")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_line = f"⚡ DATOS SIMULADOS | Actualizaciones: {self.update_count} | Timestamp: {timestamp}"
        print(f"║ {info_line:<{width-3}}║")
        print("╠" + "═" * (width - 2) + "╣")

    def render_section(self, title, data_dict, width=120):
        """Renderiza una sección genérica"""
        print("║ " + title + " " * (width - 4 - len(title)) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        for key, value in data_dict.items():
            line = f"║   {key:<30} {str(value)[:80]}"
            print(f"{line:<{width-1}}║")

    def render_imu_section(self, imu_data):
        """Renderiza sección de IMU"""
        width = 120
        print("║ 🧭 IMU (INERTIAL MEASUREMENT UNIT)" + " " * (width - 38) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        # Cuaternión
        q = imu_data["quaternion"]
        line = f"║   Cuaternión:    W={q[0]:>7.4f}  X={q[1]:>7.4f}  Y={q[2]:>7.4f}  Z={q[3]:>7.4f}"
        print(f"{line:<{width-1}}║")

        # Roll, Pitch, Yaw
        rpy = imu_data["rpy"]
        roll_deg = rpy[0] * 57.2958
        pitch_deg = rpy[1] * 57.2958
        yaw_deg = rpy[2] * 57.2958
        line = f"║   Orientación:   Roll={roll_deg:>7.2f}°  Pitch={pitch_deg:>7.2f}°  Yaw={yaw_deg:>7.2f}°"
        print(f"{line:<{width-1}}║")

        # Giroscopio
        gyro = imu_data["gyroscope"]
        line = f"║   Giroscopio:    X={gyro[0]:>7.4f}  Y={gyro[1]:>7.4f}  Z={gyro[2]:>7.4f} rad/s"
        print(f"{line:<{width-1}}║")

        # Acelerómetro
        accel = imu_data["accelerometer"]
        line = f"║   Acelerómetro:  X={accel[0]:>7.4f}  Y={accel[1]:>7.4f}  Z={accel[2]:>7.4f} m/s²"
        print(f"{line:<{width-1}}║")

        # Temperatura
        temp = imu_data["temperature"]
        line = f"║   Temperatura:   {temp:.2f}°C"
        print(f"{line:<{width-1}}║")

    def render_position_section(self, position_data):
        """Renderiza sección de posición"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 📍 POSICIÓN Y VELOCIDAD" + " " * (width - 27) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        pos = position_data["position"]
        line = f"║   Posición:      X={pos[0]:>7.3f}m  Y={pos[1]:>7.3f}m  Z={pos[2]:>7.3f}m"
        print(f"{line:<{width-1}}║")

        vel = position_data["velocity"]
        line = f"║   Velocidad:     Vx={vel[0]:>7.3f}  Vy={vel[1]:>7.3f}  Vz={vel[2]:>7.3f} m/s"
        print(f"{line:<{width-1}}║")

        yaw_speed = position_data["yaw_speed"]
        line = f"║   Yaw Speed:     {yaw_speed:.4f} rad/s"
        print(f"{line:<{width-1}}║")

        body_height = position_data["body_height"]
        line = f"║   Altura cuerpo: {body_height:.3f}m"
        print(f"{line:<{width-1}}║")

    def render_mode_section(self, mode_data):
        """Renderiza sección de modo"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ ⚙️  MODO Y ESTADO DEL ROBOT" + " " * (width - 31) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        mode_names = {0: "Idle", 1: "Damping", 2: "Recovery Stand", 3: "Stand Up",
                     4: "Walk", 5: "Run", 6: "Climb Stairs", 7: "Trot"}
        mode_name = mode_names.get(mode_data["mode"], f"Unknown ({mode_data['mode']})")
        line = f"║   Modo actual:   {mode_name}"
        print(f"{line:<{width-1}}║")

        gait_names = {0: "Idle", 1: "Trot", 2: "Trot Running", 3: "Climb Stair"}
        gait_name = gait_names.get(mode_data["gait_type"], f"Unknown ({mode_data['gait_type']})")
        line = f"║   Tipo marcha:   {gait_name}"
        print(f"{line:<{width-1}}║")

        progress = mode_data["progress"]
        bar_length = 40
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        line = f"║   Progreso:      [{bar}] {progress*100:.1f}%"
        print(f"{line:<{width-1}}║")

        foot_raise = mode_data["foot_raise_height"]
        line = f"║   Elevación:     {foot_raise:.3f}m"
        print(f"{line:<{width-1}}║")

    def render_obstacles_section(self, obstacles):
        """Renderiza sección de obstáculos"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 🚧 DETECCIÓN DE OBSTÁCULOS" + " " * (width - 30) + "║")
        print("╠" + "─" * (width - 2) + "╣")

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

        min_dist = min(obstacles)
        if min_dist < 0.3:
            warning = "⚠️  ALERTA: Obstáculo muy cercano!"
        elif min_dist < 0.5:
            warning = "⚡ Precaución: Obstáculo cerca"
        else:
            warning = "✅ Zona despejada"
        line = f"║   Estado: {warning}"
        print(f"{line:<{width-1}}║")

    def render_foot_section(self, foot_data):
        """Renderiza sección de patas"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 🦿 ESTADO DE LAS PATAS" + " " * (width - 26) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        forces = foot_data["foot_force"]
        line = f"║   Fuerza:        FL={forces[0]:>6.2f}N  FR={forces[1]:>6.2f}N  RL={forces[2]:>6.2f}N  RR={forces[3]:>6.2f}N"
        print(f"{line:<{width-1}}║")

        max_force = max(forces)
        for i, (name, force) in enumerate(zip(["FL (Frente Izq)", "FR (Frente Der)",
                                                 "RL (Atrás Izq)", "RR (Atrás Der)"], forces)):
            bar_length = 30
            filled = int(bar_length * (force / max_force)) if max_force > 0 else 0
            bar = "█" * filled + "░" * (bar_length - filled)
            line = f"║   {name:<15} [{bar}] {force:>6.2f}N"
            print(f"{line:<{width-1}}║")

    def render_battery_section(self, battery_data):
        """Renderiza sección de batería"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 🔋 BATERÍA (BMS)" + " " * (width - 19) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        soc = battery_data["soc"]
        bar_length = 40
        filled = int(bar_length * soc / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        icon = "🟢" if soc > 60 else "🟡" if soc > 30 else "🔴"
        line = f"║   Carga:         {icon} [{bar}] {soc:.1f}%"
        print(f"{line:<{width-1}}║")

        voltage = battery_data["voltage"]
        current = battery_data["current"]
        power = voltage * current
        line = f"║   Voltaje:       {voltage:.2f}V  |  Corriente: {current:.2f}A  |  Potencia: {power:.2f}W"
        print(f"{line:<{width-1}}║")

        cycles = battery_data["cycle_count"]
        line = f"║   Ciclos carga:  {cycles}"
        print(f"{line:<{width-1}}║")

        temps = battery_data["temperature"]
        temp_str = "  ".join([f"T{i+1}:{t:.1f}°C" for i, t in enumerate(temps)])
        line = f"║   Temperaturas:  {temp_str}"
        print(f"{line:<{width-1}}║")

    def render_motors_summary(self, motors_data):
        """Renderiza resumen de motores"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ ⚙️  ESTADO DE MOTORES (20 MOTORES)" + " " * (width - 38) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        leg_names = ["FL (Frente Izq)", "FR (Frente Der)", "RL (Atrás Izq)", "RR (Atrás Der)"]
        for leg_idx, leg_name in enumerate(leg_names):
            start_idx = leg_idx * 3
            leg_motors = motors_data[start_idx:start_idx+3]

            avg_temp = sum(m["temperature"] for m in leg_motors) / len(leg_motors)
            temp_icon = "🔴" if avg_temp > 60 else "🟡" if avg_temp > 45 else "🟢"

            line = f"║   {leg_name:<15} Temp: {temp_icon} {avg_temp:.1f}°C"
            print(f"{line:<{width-1}}║")

        hot_motors = [i for i, m in enumerate(motors_data) if m["temperature"] > 60]
        if hot_motors:
            line = f"║   ⚠️  Motores calientes: {', '.join(map(str, hot_motors))}"
            print(f"{line:<{width-1}}║")
        else:
            line = "║   ✅ Todos los motores operando normalmente"
            print(f"{line:<{width-1}}║")

    def render_system_section(self, system_data):
        """Renderiza sección de sistema"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        print("║ 💻 INFORMACIÓN DEL SISTEMA" + " " * (width - 30) + "║")
        print("╠" + "─" * (width - 2) + "╣")

        power_v = system_data["power_v"]
        power_a = system_data["power_a"]
        line = f"║   Alimentación:  {power_v:.2f}V @ {power_a:.2f}A"
        print(f"{line:<{width-1}}║")

        ntc1 = system_data["temperature_ntc1"]
        ntc2 = system_data["temperature_ntc2"]
        line = f"║   Temp. NTC:     NTC1: {ntc1:.1f}°C  |  NTC2: {ntc2:.1f}°C"
        print(f"{line:<{width-1}}║")

        fans = system_data["fan_frequency"]
        fan_str = "  ".join([f"Fan{i+1}:{f}Hz" for i, f in enumerate(fans)])
        line = f"║   Ventiladores:  {fan_str}"
        print(f"{line:<{width-1}}║")

        sn = system_data["sn"]
        version = system_data["version"]
        version_str = ".".join(map(str, version))
        line = f"║   S/N: {sn}  |  Versión: {version_str}"
        print(f"{line:<{width-1}}║")

    def render_footer(self):
        """Renderiza el pie"""
        width = 120
        print("╠" + "═" * (width - 2) + "╣")
        line = "⌨️  Presiona Ctrl+C para salir  |  ⚡ Modo Simulación Activo"
        padding = (width - 2 - len(line)) // 2
        print("║" + " " * padding + line + " " * (width - 2 - padding - len(line)) + "║")
        print("╚" + "═" * (width - 2) + "╝")

    def render(self):
        """Renderiza todo el dashboard"""
        self.clear_screen()
        self.update_count += 1
        self.time += 0.5

        # Generar datos simulados
        imu_data = self.generate_imu_data()
        position_data = self.generate_position_data()
        mode_data = self.generate_mode_data()
        obstacles = self.generate_obstacles()
        foot_data = self.generate_foot_data()
        battery_data = self.generate_battery_data()
        motors_data = self.generate_motors_data()
        system_data = self.generate_system_data()

        # Renderizar
        self.render_header()
        self.render_imu_section(imu_data)
        self.render_position_section(position_data)
        self.render_mode_section(mode_data)
        self.render_obstacles_section(obstacles)
        self.render_foot_section(foot_data)
        self.render_battery_section(battery_data)
        self.render_motors_summary(motors_data)
        self.render_system_section(system_data)
        self.render_footer()

    async def run(self):
        """Ejecuta el dashboard"""
        self.running = True

        while self.running:
            self.render()
            await asyncio.sleep(0.5)


async def main():
    """Función principal"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║    🤖 DEMO DE TELEMETRÍA (DATOS SIMULADOS)                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print("✅ Iniciando dashboard con datos simulados...")
    print("   (Útil para desarrollo sin robot físico)")
    print()
    await asyncio.sleep(2)

    dashboard = SimulatedTelemetryDashboard()

    try:
        await dashboard.run()

    except KeyboardInterrupt:
        print("\n\n⚠️  Deteniendo dashboard...")

    finally:
        dashboard.running = False
        print("\n👋 ¡Hasta pronto!\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Adiós!")
