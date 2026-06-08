#!/usr/bin/env python3
"""
Go2 Telemetry Monitor - todo en uno

Lee:
- sportmodestate: position, velocity, yaw_speed, IMU quaternion/rpy/gyro/accel, obstáculos
- lowstate: batería, voltaje, motores, fuerza en patas

También guarda CSV básico para análisis posterior.
"""

import argparse
import asyncio
import csv
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional

from unitree_webrtc_connect import (
    UnitreeWebRTCConnection,
    WebRTCConnectionMethod,
    RTC_TOPIC,
)


STATE: Dict[str, Any] = {
    "sport": None,
    "low": None,
    "last_print": 0.0,
    "last_csv": 0.0,
}


def safe_get(data: Optional[dict], key: str, default=None):
    if not isinstance(data, dict):
        return default
    return data.get(key, default)


def fmt(value, ndigits=4):
    if value is None:
        return "None"

    if isinstance(value, float):
        return f"{value:.{ndigits}f}"

    if isinstance(value, int):
        return str(value)

    if isinstance(value, list):
        out = []
        for x in value:
            if isinstance(x, float):
                out.append(round(x, ndigits))
            else:
                out.append(x)
        return str(out)

    return str(value)


def extract_message_data(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    En los ejemplos oficiales, el callback recibe un dict con message["data"].
    Pero dejo fallback por si llega plano.
    """
    if isinstance(message, dict) and "data" in message and isinstance(message["data"], dict):
        return message["data"]
    return message


def clear_screen():
    sys.stdout.write("\033[H\033[J")


def print_dashboard(no_clear: bool = False):
    sport = STATE["sport"] or {}
    low = STATE["low"] or {}

    imu = safe_get(sport, "imu_state", {}) or {}

    position = safe_get(sport, "position")
    velocity = safe_get(sport, "velocity")
    yaw_speed = safe_get(sport, "yaw_speed")
    body_height = safe_get(sport, "body_height")
    range_obstacle = safe_get(sport, "range_obstacle")
    foot_force_sport = safe_get(sport, "foot_force")

    quaternion = safe_get(imu, "quaternion")
    rpy = safe_get(imu, "rpy")
    gyroscope = safe_get(imu, "gyroscope")
    accelerometer = safe_get(imu, "accelerometer")
    imu_temp = safe_get(imu, "temperature")

    mode = safe_get(sport, "mode")
    gait_type = safe_get(sport, "gait_type")

    bms = safe_get(low, "bms_state", {}) or {}
    motor_state = safe_get(low, "motor_state", []) or []
    foot_force_low = safe_get(low, "foot_force")
    power_v = safe_get(low, "power_v")
    power_a = safe_get(low, "power_a")
    temp_ntc1 = safe_get(low, "temperature_ntc1")
    temp_ntc2 = safe_get(low, "temperature_ntc2")

    if not no_clear:
        clear_screen()

    print("============================================================")
    print("🤖 UNITREE GO2 TELEMETRY MONITOR")
    print("============================================================")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print("📍 ODOMETRÍA CANDIDATA / SPORT MODE STATE")
    print("------------------------------------------------------------")
    print(f"Mode:            {fmt(mode)}")
    print(f"Gait type:       {fmt(gait_type)}")
    print(f"Position [x,y,z]:{fmt(position)}")
    print(f"Velocity:        {fmt(velocity)}")
    print(f"Yaw speed:       {fmt(yaw_speed)}")
    print(f"Body height:     {fmt(body_height)}")
    print(f"Obstacles range: {fmt(range_obstacle)}")
    print(f"Foot force:      {fmt(foot_force_sport)}")
    print()

    print("🧭 IMU")
    print("------------------------------------------------------------")
    print(f"RPY [r,p,y]:     {fmt(rpy)}")
    print(f"Quaternion:      {fmt(quaternion)}")
    print(f"Gyroscope:       {fmt(gyroscope)}")
    print(f"Accelerometer:   {fmt(accelerometer)}")
    print(f"IMU temp:        {fmt(imu_temp)}")
    print()

    print("🔋 LOWSTATE / BATERÍA / ENERGÍA")
    print("------------------------------------------------------------")
    print(f"SOC:             {fmt(safe_get(bms, 'soc'))}%")
    print(f"BMS current:     {fmt(safe_get(bms, 'current'))} mA")
    print(f"Cycle count:     {fmt(safe_get(bms, 'cycle'))}")
    print(f"Power V:         {fmt(power_v)} V")
    print(f"Power A:         {fmt(power_a)} A")
    print(f"Temp NTC1:       {fmt(temp_ntc1)}")
    print(f"Temp NTC2:       {fmt(temp_ntc2)}")
    print(f"Foot force low:  {fmt(foot_force_low)}")
    print()

    print("⚙️ MOTORES")
    print("------------------------------------------------------------")
    if motor_state:
        for i, motor in enumerate(motor_state[:12]):
            q = safe_get(motor, "q")
            dq = safe_get(motor, "dq")
            temp = safe_get(motor, "temperature")
            lost = safe_get(motor, "lost")
            print(
                f"Motor {i + 1:02}: "
                f"q={fmt(q)}  dq={fmt(dq)}  temp={fmt(temp)}°C  lost={fmt(lost)}"
            )
    else:
        print("Todavía sin motor_state.")

    print()
    print("Presiona Ctrl+C para salir.")
    sys.stdout.flush()


def flatten_list(value, index, default=None):
    if isinstance(value, list) and len(value) > index:
        return value[index]
    return default


def write_csv_row(csv_writer, csv_file):
    sport = STATE["sport"] or {}
    low = STATE["low"] or {}

    imu = safe_get(sport, "imu_state", {}) or {}
    bms = safe_get(low, "bms_state", {}) or {}

    position = safe_get(sport, "position")
    velocity = safe_get(sport, "velocity")
    rpy = safe_get(imu, "rpy")
    quaternion = safe_get(imu, "quaternion")
    gyro = safe_get(imu, "gyroscope")
    accel = safe_get(imu, "accelerometer")
    obstacles = safe_get(sport, "range_obstacle")

    row = {
        "timestamp_unix": time.time(),
        "timestamp_iso": datetime.now().isoformat(),

        "pos_x": flatten_list(position, 0),
        "pos_y": flatten_list(position, 1),
        "pos_z": flatten_list(position, 2),

        "vel_x": flatten_list(velocity, 0),
        "vel_y": flatten_list(velocity, 1),
        "vel_z": flatten_list(velocity, 2),

        "roll": flatten_list(rpy, 0),
        "pitch": flatten_list(rpy, 1),
        "yaw": flatten_list(rpy, 2),

        "quat_w": flatten_list(quaternion, 0),
        "quat_x": flatten_list(quaternion, 1),
        "quat_y": flatten_list(quaternion, 2),
        "quat_z": flatten_list(quaternion, 3),

        "gyro_x": flatten_list(gyro, 0),
        "gyro_y": flatten_list(gyro, 1),
        "gyro_z": flatten_list(gyro, 2),

        "acc_x": flatten_list(accel, 0),
        "acc_y": flatten_list(accel, 1),
        "acc_z": flatten_list(accel, 2),

        "yaw_speed": safe_get(sport, "yaw_speed"),
        "body_height": safe_get(sport, "body_height"),
        "mode": safe_get(sport, "mode"),
        "gait_type": safe_get(sport, "gait_type"),

        "obstacle_0": flatten_list(obstacles, 0),
        "obstacle_1": flatten_list(obstacles, 1),
        "obstacle_2": flatten_list(obstacles, 2),
        "obstacle_3": flatten_list(obstacles, 3),

        "battery_soc": safe_get(bms, "soc"),
        "battery_current_ma": safe_get(bms, "current"),
        "power_v": safe_get(low, "power_v"),
        "power_a": safe_get(low, "power_a"),
    }

    csv_writer.writerow(row)
    csv_file.flush()


def make_sport_callback(args, csv_writer, csv_file):
    def sport_callback(message):
        STATE["sport"] = extract_message_data(message)

        now = time.time()

        if csv_writer and csv_file and now - STATE["last_csv"] >= (1.0 / args.csv_hz):
            write_csv_row(csv_writer, csv_file)
            STATE["last_csv"] = now

        if now - STATE["last_print"] >= (1.0 / args.print_hz):
            print_dashboard(no_clear=args.no_clear)
            STATE["last_print"] = now

    return sport_callback


def lowstate_callback(message):
    STATE["low"] = extract_message_data(message)


def connection_method_from_arg(method: str):
    method = method.lower().strip()

    if method in ["sta", "localsta", "wifi", "lan"]:
        return WebRTCConnectionMethod.LocalSTA

    if method in ["ap", "localap"]:
        return WebRTCConnectionMethod.LocalAP

    raise ValueError("Método inválido. Usa: sta o ap")


def open_csv(path: Optional[str]):
    if not path:
        return None, None

    fieldnames = [
        "timestamp_unix",
        "timestamp_iso",
        "pos_x",
        "pos_y",
        "pos_z",
        "vel_x",
        "vel_y",
        "vel_z",
        "roll",
        "pitch",
        "yaw",
        "quat_w",
        "quat_x",
        "quat_y",
        "quat_z",
        "gyro_x",
        "gyro_y",
        "gyro_z",
        "acc_x",
        "acc_y",
        "acc_z",
        "yaw_speed",
        "body_height",
        "mode",
        "gait_type",
        "obstacle_0",
        "obstacle_1",
        "obstacle_2",
        "obstacle_3",
        "battery_soc",
        "battery_current_ma",
        "power_v",
        "power_a",
    ]

    csv_file = open(path, "w", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    csv_file.flush()
    return writer, csv_file


async def main():
    parser = argparse.ArgumentParser(description="Unitree Go2 telemetry monitor")
    parser.add_argument(
        "--ip",
        default=os.environ.get("UNITREE_ROBOT_IP", "192.168.12.1"),
        help="IP del robot. Default: UNITREE_ROBOT_IP o 192.168.12.1",
    )
    parser.add_argument(
        "--method",
        default=os.environ.get("UNITREE_CONNECTION_METHOD", "sta"),
        choices=["sta", "ap"],
        help="Método de conexión: sta para red local/WiFi, ap para hotspot del robot.",
    )
    parser.add_argument(
        "--aes-key",
        default=os.environ.get("UNITREE_AES_128_KEY"),
        help="AES key para firmware Go2 1.1.15+. También puede venir de UNITREE_AES_128_KEY.",
    )
    parser.add_argument(
        "--csv",
        default="go2_telemetry.csv",
        help="Archivo CSV de salida. Usa '' para desactivar.",
    )
    parser.add_argument(
        "--print-hz",
        type=float,
        default=5.0,
        help="Frecuencia de actualización de terminal.",
    )
    parser.add_argument(
        "--csv-hz",
        type=float,
        default=10.0,
        help="Frecuencia de guardado CSV.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Duración en segundos. 0 = infinito.",
    )
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="No limpiar la terminal entre actualizaciones.",
    )

    args = parser.parse_args()

    if args.csv == "":
        args.csv = None

    method = connection_method_from_arg(args.method)

    kwargs = {}

    if method == WebRTCConnectionMethod.LocalSTA:
        kwargs["ip"] = args.ip

    if args.aes_key:
        kwargs["aes_128_key"] = args.aes_key

    csv_writer, csv_file = open_csv(args.csv)

    print("============================================================")
    print("🤖 Conectando a Unitree Go2")
    print("============================================================")
    print(f"Método: {method}")
    print(f"IP: {args.ip if method == WebRTCConnectionMethod.LocalSTA else '(AP default)'}")
    print(f"AES key: {'sí' if args.aes_key else 'no'}")
    print(f"CSV: {args.csv if args.csv else 'desactivado'}")
    print("============================================================")

    conn = UnitreeWebRTCConnection(method, **kwargs)

    try:
        await conn.connect()
        print("✅ Conexión WebRTC establecida.")
        print("Suscribiendo tópicos...")

        conn.datachannel.pub_sub.subscribe(
            RTC_TOPIC["LF_SPORT_MOD_STATE"],
            make_sport_callback(args, csv_writer, csv_file),
        )

        conn.datachannel.pub_sub.subscribe(
            RTC_TOPIC["LOW_STATE"],
            lowstate_callback,
        )

        print("✅ Suscrito a:")
        print(f"   - {RTC_TOPIC['LF_SPORT_MOD_STATE']}")
        print(f"   - {RTC_TOPIC['LOW_STATE']}")
        print("Leyendo telemetría...")

        if args.duration and args.duration > 0:
            await asyncio.sleep(args.duration)
        else:
            while True:
                await asyncio.sleep(1)

    finally:
        try:
            await conn.disconnect()
        except Exception:
            pass

        if csv_file:
            csv_file.close()

        print("\nConexión cerrada.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nRevisa:")
        print("1. Que el robot esté encendido y completamente iniciado.")
        print("2. Que estés en la misma red/WiFi que el robot.")
        print("3. Que la IP sea correcta.")
        print("4. Que la app oficial de Unitree no esté conectada al mismo tiempo.")
        print("5. Si tu firmware es Go2 1.1.15+, configura UNITREE_AES_128_KEY.")
        sys.exit(1)
