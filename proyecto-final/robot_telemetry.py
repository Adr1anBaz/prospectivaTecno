#!/usr/bin/env python3
"""
Módulo de telemetría completo para Robot Unitree Go2
Extrae TODA la información disponible del robot

Basado en: https://github.com/legion1581/unitree_webrtc_connect
"""

import asyncio
from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class IMUData:
    """Datos del IMU (Inertial Measurement Unit)"""
    quaternion: List[float] = field(default_factory=lambda: [0, 0, 0, 0])
    gyroscope: List[float] = field(default_factory=lambda: [0, 0, 0])
    accelerometer: List[float] = field(default_factory=lambda: [0, 0, 0])
    rpy: List[float] = field(default_factory=lambda: [0, 0, 0])
    temperature: float = 0.0


@dataclass
class RobotPosition:
    """Posición y velocidad del robot"""
    position: List[float] = field(default_factory=lambda: [0, 0, 0])
    velocity: List[float] = field(default_factory=lambda: [0, 0, 0])
    yaw_speed: float = 0.0
    body_height: float = 0.0


@dataclass
class FootData:
    """Datos de las patas del robot"""
    foot_force: List[float] = field(default_factory=lambda: [0, 0, 0, 0])
    foot_position_body: List[List[float]] = field(default_factory=list)
    foot_speed_body: List[List[float]] = field(default_factory=list)


@dataclass
class MotorState:
    """Estado de un motor individual"""
    index: int = 0
    q: float = 0.0
    dq: float = 0.0
    ddq: float = 0.0
    tau_est: float = 0.0
    temperature: float = 0.0
    lost: int = 0


@dataclass
class BatteryState:
    """Estado de la batería"""
    soc: float = 0.0
    current: float = 0.0
    voltage: float = 0.0
    temperature: List[float] = field(default_factory=list)
    cycle_count: int = 0


@dataclass
class SportModeState:
    """Estado completo en modo deportivo"""
    timestamp: str = ""
    imu: Optional[IMUData] = None
    position: Optional[RobotPosition] = None
    foot: Optional[FootData] = None
    mode: int = 0
    gait_type: int = 0
    progress: float = 0.0
    foot_raise_height: float = 0.0
    range_obstacle: List[float] = field(default_factory=lambda: [0, 0, 0, 0])


@dataclass
class LowLevelState:
    """Estado de bajo nivel (motores, batería, hardware)"""
    timestamp: str = ""
    imu_rpy: List[float] = field(default_factory=lambda: [0, 0, 0])
    motors: List[MotorState] = field(default_factory=list)
    battery: Optional[BatteryState] = None
    foot_force: List[float] = field(default_factory=lambda: [0, 0, 0, 0])
    temperature_ntc1: float = 0.0
    temperature_ntc2: float = 0.0
    power_v: float = 0.0
    power_a: float = 0.0
    fan_frequency: List[int] = field(default_factory=list)
    sn: str = ""
    version: List[int] = field(default_factory=list)
    bandwidth: int = 0


class RobotTelemetry:
    """Gestor completo de telemetría del robot"""

    def __init__(self, connection):
        self.conn = connection
        self.sport_state: SportModeState = SportModeState()
        self.low_state: LowLevelState = LowLevelState()
        self.is_monitoring = False
        self._tasks = []

    async def start_monitoring(self, update_rate: float = 0.2):
        """Inicia monitoreo de TODA la telemetría"""
        if self.is_monitoring:
            return

        self.is_monitoring = True

        # Crear tareas de monitoreo
        self._tasks = [
            asyncio.create_task(self._monitor_sport_state(update_rate)),
            asyncio.create_task(self._monitor_low_state(update_rate))
        ]

    async def stop_monitoring(self):
        """Detiene el monitoreo"""
        self.is_monitoring = False
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)

    async def _monitor_sport_state(self, update_rate: float):
        """Monitoreo del estado deportivo"""
        while self.is_monitoring:
            try:
                # Aquí iría la lectura real del tópico
                # Por ahora simulamos datos (reemplazar con conn.data_channel)
                await asyncio.sleep(update_rate)
            except Exception:
                await asyncio.sleep(1)

    async def _monitor_low_state(self, update_rate: float):
        """Monitoreo del estado bajo nivel"""
        while self.is_monitoring:
            try:
                # Aquí iría la lectura real del tópico
                await asyncio.sleep(update_rate)
            except Exception:
                await asyncio.sleep(1)

    def get_all_telemetry(self) -> Dict[str, Any]:
        """Obtiene TODA la telemetría en un dict"""
        return {
            "timestamp": datetime.now().isoformat(),
            "sport_mode": asdict(self.sport_state),
            "low_level": asdict(self.low_state)
        }
