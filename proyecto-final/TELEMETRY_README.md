# 📡 Sistema de Telemetría Completo - Unitree Go2

Dashboard en tiempo real que muestra **TODA** la información disponible del robot Unitree Go2.

---

## 🚀 Uso Rápido

### Opción 1: Demo con Datos Simulados (SIN ROBOT)

```bash
# Ejecutar dashboard con datos simulados
uv run python telemetry_demo.py
```

✅ **Recomendado para:** Desarrollo, testing, demostraciones sin hardware

### Opción 2: Dashboard Real (CON ROBOT)

```bash
# 1. Conectarse al WiFi del robot
#    Red: Unitree_XXXXX

# 2. Verificar conexión primero
uv run python test_connection.py

# 3. Ejecutar dashboard
uv run python telemetry_dashboard.py
```

⚠️ **Requiere:** Robot físico encendido y conectado

---

## 📊 Información Mostrada

### 🧭 IMU (Inertial Measurement Unit)
- **Cuaternión** [W, X, Y, Z] - Orientación en 4D
- **Roll, Pitch, Yaw** - Orientación en grados
- **Giroscopio** [X, Y, Z] - Velocidad angular (rad/s)
- **Acelerómetro** [X, Y, Z] - Aceleración (m/s²)
- **Temperatura** - Temperatura del sensor IMU (°C)

### 📍 Posición y Velocidad
- **Posición** [X, Y, Z] - Posición estimada (metros)
- **Velocidad** [Vx, Vy, Vz] - Velocidad lineal (m/s)
- **Yaw Speed** - Velocidad de giro (rad/s)
- **Altura Corporal** - Altura del centro del robot (metros)

### ⚙️ Modo y Estado del Robot
- **Modo Actual**
  - 0: Idle (Inactivo)
  - 1: Damping (Amortiguación)
  - 2: Recovery Stand (Recuperación)
  - 3: Stand Up (De pie)
  - 4: Walk (Caminar)
  - 5: Run (Correr)
  - 6: Climb Stairs (Subir escaleras)
  - 7: Trot (Trote)
  - 8-11: Modos especiales

- **Tipo de Marcha**
  - 0: Idle
  - 1: Trot (Trote normal)
  - 2: Trot Running (Trote corriendo)
  - 3: Climb Stair (Subir escalera)
  - 4: Trot Obstacle (Trote con obstáculos)

- **Progreso** - Progreso de acción actual (0-100%)
- **Elevación de Patas** - Altura de elevación (metros)

### 🚧 Detección de Obstáculos
- **Frente** - Distancia a obstáculo frontal
- **Atrás** - Distancia a obstáculo trasero
- **Izquierda** - Distancia a obstáculo izquierdo
- **Derecha** - Distancia a obstáculo derecho

**Códigos de color:**
- 🟢 > 0.5m - Zona segura
- 🟡 0.3-0.5m - Precaución
- 🔴 < 0.3m - ALERTA

### 🦿 Estado de las Patas
- **Fuerza en Patas** [FL, FR, RL, RR] - Newtons
  - FL: Front Left (Frente Izquierda)
  - FR: Front Right (Frente Derecha)
  - RL: Rear Left (Atrás Izquierda)
  - RR: Rear Right (Atrás Derecha)

- **Posición Relativa** - Posición de cada pata respecto al cuerpo
- **Velocidad Relativa** - Velocidad de cada pata respecto al cuerpo

### 🔋 Batería (BMS - Battery Management System)
- **Nivel de Carga** - State of Charge (SOC) en %
- **Voltaje** - Voltaje actual (V)
- **Corriente** - Corriente de descarga/carga (A)
- **Potencia** - Potencia instantánea (W)
- **Ciclos de Carga** - Número total de ciclos
- **Temperaturas** - Temperatura de cada celda (°C)

**Códigos de color:**
- 🟢 > 60% - Batería buena
- 🟡 30-60% - Batería media
- 🔴 < 30% - Batería baja

### ⚙️ Motores (20 motores totales)
**Para cada motor:**
- **Posición Angular** (q) - Radianes
- **Velocidad Angular** (dq) - rad/s
- **Aceleración Angular** (ddq) - rad/s²
- **Torque Estimado** (tau_est) - N·m
- **Temperatura** - °C
- **Estado de Comunicación** (lost) - 0=OK, >0=Problema

**Organización por pata:**
- 3 motores por pata (cadera, muslo, rodilla)
- Total: 12 motores para patas + 8 adicionales

**Alertas automáticas:**
- 🔴 Motores > 60°C
- ❌ Motores con pérdida de comunicación

### 💻 Información del Sistema
- **Voltaje de Alimentación** - Voltaje del sistema (V)
- **Corriente de Alimentación** - Corriente total (A)
- **Temperatura NTC1** - Sensor de temperatura 1 (°C)
- **Temperatura NTC2** - Sensor de temperatura 2 (°C)
- **Frecuencia de Ventiladores** - Hz de cada ventilador
- **Número de Serie** - Identificador único del robot
- **Versión de Firmware** - Versión del sistema

### 🎮 Control Inalámbrico
- **Joystick Izquierdo** - [X, Y] normalizado (-1 a 1)
- **Joystick Derecho** - [X, Y] normalizado (-1 a 1)
- **Botones** - Estado de botones en hexadecimal

---

## 🔧 Tópicos ROS2/WebRTC Monitoreados

El dashboard se suscribe a:

```python
RTC_TOPIC["LF_SPORT_MOD_STATE"]    # rt/lf/sportmodestate
RTC_TOPIC["LOW_STATE"]              # rt/lf/lowstate
RTC_TOPIC["WIRELESS_CONTROLLER"]    # rt/wirelesscontroller
```

---

## 📝 Archivos del Proyecto

```
proyecto-final/
├── telemetry_dashboard.py    # 📊 Dashboard completo (MAIN)
├── robot_telemetry.py         # 📡 Módulo de telemetría
└── TELEMETRY_README.md        # 📖 Esta documentación
```

---

## 🎯 Ejemplos de Uso

### Uso Básico

```bash
# Conectar WiFi del robot y ejecutar
uv run python telemetry_dashboard.py
```

### Con IP Personalizada

```bash
# Configurar IP del robot
export UNITREE_ROBOT_IP="192.168.12.15"

# Ejecutar
uv run python telemetry_dashboard.py
```

### Monitoreo Largo

```bash
# Ejecutar y dejar corriendo
# El dashboard se actualiza cada 0.5 segundos
# Presiona Ctrl+C para salir
uv run python telemetry_dashboard.py
```

---

## 🔍 Solución de Problemas

### ❌ "Error al conectar"

1. Verifica conexión WiFi al robot
2. Prueba primero con `test_connection.py`
3. Verifica que el robot esté completamente iniciado (60s después del pitido)

### ⚠️ "No hay datos disponibles"

- El robot puede tardar unos segundos en empezar a transmitir
- Algunos datos solo están disponibles cuando el robot está en ciertos modos
- Verifica que el firmware del robot sea compatible

### 🐌 Dashboard lento

- El dashboard se actualiza cada 0.5s por defecto
- Ajusta `update_rate` en el código si necesitas más/menos frecuencia
- Considera la carga de red del WiFi del robot

---

## 📚 Referencias

- **Librería base:** [unitree_webrtc_connect](https://github.com/legion1581/unitree_webrtc_connect)
- **Documentación Unitree:** [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2)
- **Tópicos disponibles:** Ver `unitree_webrtc_connect/constants.py`

---

## 🚧 Desarrollo Futuro

Posibles mejoras:

- [ ] Agregar soporte para LiDAR (`ULIDAR_ARRAY`)
- [ ] Streaming de video de cámara
- [ ] Exportación continua a archivo CSV/JSON
- [ ] Gráficas en tiempo real con matplotlib
- [ ] Dashboard web con Flask/FastAPI
- [ ] Logging de telemetría para análisis posterior
- [ ] Alertas configurables (temperatura, batería, obstáculos)

---

## 💡 Notas Técnicas

- **Frecuencia de actualización:** 0.5s (2 Hz) por defecto
- **Protocolo:** WebRTC sobre WiFi local
- **Formato de datos:** Los datos vienen en formato protobuf/JSON desde el robot
- **Compatible con:** Unitree Go2 (todas las variantes)

---

## 🤝 Contribuciones

Este es un módulo independiente que puede usarse:
- ✅ Solo (dashboard de telemetría)
- ✅ Integrado con sistema de voz
- ✅ Como base para tu propio sistema de monitoreo

---

## ⚡ Quick Reference

```bash
# Conectar al robot
WiFi: Unitree_XXXXX

# Ejecutar dashboard
uv run python telemetry_dashboard.py

# Salir
Ctrl+C
```

**¡Disfruta monitoreando tu robot! 🤖📊**
