# Guía de Simulación — Unitree Go2 AIR + MuJoCo + ROS 2

## Cómo probar el control por voz en simulacion antes del hardware real

---

## Tabla de Contenidos

1. [Arquitectura del Pipeline](#1-arquitectura-del-pipeline)
2. [Requisitos Previos](#2-requisitos-previos)
3. [Configuración Automática del Entorno](#3-configuración-automática-del-entorno)
4. [Estructura de Archivos](#4-estructura-de-archivos)
5. [Ejecución Paso a Paso](#5-ejecución-paso-a-paso)
6. [Comandos de Voz Soportados](#6-comandos-de-voz-soportados)
7. [Depuración y Solución de Problemas](#7-depuración-y-solución-de-problemas)
8. [Del Simulador al Hardware Real](#8-del-simulador-al-hardware-real)
9. [Roadmap: Navegación Autónoma](#9-roadmap-navegación-autónoma)

---

## 1. Arquitectura del Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     PIPELINE COMPLETO                            │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐ │
│  │ Micrófono │───▶│ Whisper  │───▶│  Ollama  │───▶│ Tool Call │ │
│  │ (voz)    │    │ (STT)    │    │ (LLM)    │    │ (JSON)    │ │
│  └──────────┘    └──────────┘    └──────────┘    └─────┬─────┘ │
│                                                        │       │
│                                          ┌─────────────▼─────┐ │
│                                          │ robot_tools.py    │ │
│                                          │ (validate + post- │ │
│                                          │  process)         │ │
│                                          └─────────┬─────────┘ │
│                                                    │           │
│                          ┌─────────────────────────▼─────────┐ │
│                          │       CAPA DE TRANSPORTE          │ │
│                          │                                   │ │
│                          │  HARDWARE:  WebRTC → Robot Go2    │ │
│                          │  SIM:       DDS → MuJoCo         │ │
│                          └───────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Diferencia clave Sim vs Hardware

| Componente | Hardware Real | Simulación MuJoCo |
|-----------|---------------|-------------------|
| Transporte | WebRTC (WiFi AP) | CycloneDDS (loopback) |
| Conexión | `unitree_webrtc_connect` | DDS directo / `go2_sport_client` |
| IP robot | `192.168.12.1` | localhost (misma máquina) |
| Física | Robot real | MuJoCo 3.2.6 |
| Sensores | LiDAR, IMU, cámaras reales | Sensores simulados |
| Controlador | `robot_voice_controller.py` | `sim_robot_controller.py` |

**Las herramientas de IA (robot_tools.py, Whisper, Ollama) son IDÉNTICAS en ambos entornos.**

---

## 2. Requisitos Previos

### 2.1 Contenedor Distrobox

Toda la simulación corre dentro de un contenedor Distrobox con Ubuntu 22.04 y ROS 2 Humble:

```bash
# Verificar que estas dentro del contenedor
cat /etc/os-release
# PRETTY_NAME="Ubuntu 22.04.5 LTS"

echo $ROS_DISTRO
# humble
```

### 2.2 Paquetes Python (proyecto-final)

Instalar en el entorno virtual del proyecto:

```bash
cd ~/proyectoProspectiva/proyecto-final
pip install openai-whisper sounddevice numpy ollama
```

### 2.3 Ollama corriendo

El LLM debe estar activo:

```bash
# Verificar que Ollama esta instalado y corriendo
ollama list
ollama pull qwen2.5:3b   # Modelo recomendado
```

---

## 3. Configuración Automática del Entorno

Ejecuta el script autónomo **una sola vez**:

```bash
cd ~/proyectoProspectiva/ROS2-SIM
./setup_sim.sh
```

Este script:
1. Verifica ROS 2 Humble
2. Instala dependencias de sistema (GLFW, Eigen3, Boost, CycloneDDS, etc.)
3. Clona los repos Unitree (unitree_sdk2, unitree_ros2, unitree_mujoco)
4. Compila el SDK nativo
5. Descarga MuJoCo 3.2.6
6. Aplica todos los parches necesarios (Connext IDL, hack #define private public, CycloneDDS)
7. Compila el workspace completo con `colcon build`
8. Crea symlinks para archivos de modelo
9. Verifica la instalación

**Tiempo estimado**: 15-25 minutos (dependiendo de velocidad de internet y CPU).

---

## 4. Estructura de Archivos

```
~/proyectoProspectiva/
├── proyecto-final/              # Código para hardware real
│   ├── robot_tools.py           # Tools, guardrails, prompts (COMPARTIDO)
│   ├── robot_voice_controller.py # Control voz → WebRTC → Robot real
│   ├── voice_to_robot.py        # Pipeline voz → simulación mock
│   ├── test_robot_commands.py   # Tests de generación de comandos
│   └── test_sequence.py         # Secuencias de prueba
│
├── ROS2-SIM/                    # Código para simulación
│   ├── SIMULATION_SETUP.md      # Guía técnica detallada del setup
│   ├── GUIA_SIMULACION.md       # ESTE ARCHIVO — guía de uso
│   ├── setup_sim.sh             # Script autónomo de instalación
│   ├── sim_robot_controller.py  # Control voz → DDS → MuJoCo
│   ├── patches/                 # Parches aplicados al upstream
│   └── config/
│       └── cyclonedds.xml       # Configuración CycloneDDS
│
└── practicas/                   # Prácticas del curso
```

```
~/unitree_ws/                    # Workspace ROS 2 (NO se commitea)
├── src/
│   ├── unitree_ros2/            # Interfaces ROS 2
│   └── unitree_mujoco/          # Simulador MuJoCo
├── build/
│   └── unitree_mujoco/
│       └── unitree_mujoco       # ← BINARIO DEL SIMULADOR
└── install/                     # Paquetes ROS 2 instalados
```

---

## 5. Ejecución Paso a Paso

### 5.1 Iniciar el simulador MuJoCo

**Terminal 1 — El simulador debe estar corriendo primero:**

```bash
# Dentro del contenedor Distrobox
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file://$HOME/unitree_ws/src/unitree_ros2/cyclonedds_ws/src/cyclonedds.xml

# Lanzar el simulador (abre ventana GLFW)
~/unitree_ws/build/unitree_mujoco/unitree_mujoco
```

**Qué verás:**
- Una ventana azul de MuJoCo (el color de fondo por defecto)
- El robot Go2 renderizado en el centro
- En la terminal: lista de links, joints, actuadores y sensores
- El mensaje: `Mujoco data is prepared`

### 5.2 Verificar que el simulador recibe comandos (opcional)

**Terminal 2 — Prueba sin voz:**

```bash
source /opt/ros/humble/setup.bash
source ~/unitree_ws/install/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Ver paquetes disponibles
ros2 pkg list | grep unitree

# El simulador expone topics via CycloneDDS
# (los topics exactos dependen de la configuracion del bridge)
```

### 5.3 Ejecutar el controlador por voz

**Terminal 2 — Control por voz:**

```bash
cd ~/proyectoProspectiva/ROS2-SIM

# Asegurar que Ollama esta corriendo
ollama list

# Ejecutar el controlador
python3 sim_robot_controller.py
```

### 5.4 Flujo de uso

1. El programa muestra `✅ LISTO (Comando #1)`
2. Presiona **ENTER** para activar el micrófono
3. Aparece `🔴 ESCUCHANDO... (5 segundos)` — di tu comando
4. El programa transcribe con Whisper y muestra: `💬 Comando: "camina adelante"`
5. Ollama genera el tool call JSON
6. El comando se envía al simulador MuJoCo
7. **Observa el robot moverse en la ventana de MuJoCo**
8. El ciclo se repite: presiona ENTER para el siguiente comando
9. Presiona **Q + ENTER** para salir

### 5.5 Controles del simulador MuJoCo

| Tecla / Acción | Efecto |
|---------------|--------|
| Click + arrastrar | Rotar cámara |
| Shift + arrastrar | Mover cámara |
| Rueda ratón | Zoom |
| `Tab` | Cambiar modo cámara |
| `Espacio` | Pausar/Reanudar física |
| `Backspace` | Resetear simulación |
| `F1` | Ayuda de controles |

---

## 6. Comandos de Voz Soportados

### Movimiento

| Comando de voz | Acción | Tool Call |
|---------------|--------|-----------|
| "camina hacia adelante" | Avanzar | `move_robot(x=0.3, y=0, z=0)` |
| "muévete hacia atrás" | Retroceder | `move_robot(x=-0.3, y=0, z=0)` |
| "gira a la izquierda" | Rotar izq | `move_robot(x=0, y=0, z=0.5)` |
| "gira a la derecha" | Rotar der | `move_robot(x=0, y=0, z=-0.5)` |
| "muévete a la izquierda" | Lateral izq | `move_robot(x=0, y=0.3, z=0)` |
| "muévete a la derecha" | Lateral der | `move_robot(x=0, y=-0.3, z=0)` |
| "retrocede girando a la izquierda" | Compuesto | `move_robot(x=-0.2, y=0, z=0.3)` |
| "detente" / "para" | Parar | `move_robot(x=0, y=0, z=0)` |

### Animaciones

| Comando | Tool Call |
|---------|-----------|
| "levántate" / "ponte de pie" | `perform_action("StandUp")` |
| "siéntate" | `perform_action("Sit")` |
| "saluda" | `perform_action("Hello")` |
| "baila" | `perform_action("Dance1")` |
| "estírate" | `perform_action("Stretch")` |

### Modos

| Comando | Tool Call |
|---------|-----------|
| "activa el modo caminar" | `change_mode("normal")` |
| "activa el modo acrobacias" | `change_mode("ai")` |
| "apaga los motores" | `change_mode("mcf")` |
| "modo seguro" | `change_mode("mcf")` |

---

## 7. Depuración y Solución de Problemas

### El simulador crashea con `free(): invalid pointer`

**Causa**: CycloneDDS del sistema (0.10.5+shm) está tomando precedencia sobre el empaquetado (0.10.2-noshm).

**Solución**:
```bash
# Verificar que librerías se cargan
ldd ~/unitree_ws/build/unitree_mujoco/unitree_mujoco | grep ddsc
# Ambas deben apuntar a ~/unitree_sdk2/thirdparty/lib/x86_64/

# Si libddsc.so apunta a /opt/ros/humble/, reconstruir:
cd ~/unitree_ws
colcon build --packages-select unitree_mujoco \
  --cmake-args \
    -DCMAKE_BUILD_RPATH="$HOME/unitree_sdk2/thirdparty/lib/x86_64" \
    -DCMAKE_INSTALL_RPATH="$HOME/unitree_sdk2/thirdparty/lib/x86_64" \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,--disable-new-dtags"
```

### `ParseXML: Error opening file scene.xml`

**Causa**: Symlinks no creados.

**Solución**:
```bash
ln -sf ~/unitree_ws/src/unitree_mujoco/simulate/config.yaml ~/unitree_ws/build/config.yaml
ln -sfn ~/unitree_ws/src/unitree_mujoco/unitree_robots ~/unitree_ws/unitree_robots
```

### "Pantalla completamente azul en MuJoCo, no se ve el robot"

Es **normal** si el cielo/terreno no está configurado. El robot debería verse en el centro. Si no:
- La cámara puede estar lejos — usa la rueda del ratón para hacer zoom out
- Presiona `Tab` para cambiar entre modos de cámara
- Verifica que no hay errores de `ParseXML` en la terminal

### `ros2: command not found`

```bash
source /opt/ros/humble/setup.bash
```

### `ModuleNotFoundError: No module named 'robot_tools'`

El `sim_robot_controller.py` importa `robot_tools.py` desde `../proyecto-final/`. Asegúrate de ejecutarlo desde la carpeta `ROS2-SIM/`.

### Whisper no detecta el micrófono

```bash
# Listar dispositivos de audio
python3 -c "import sounddevice; print(sounddevice.query_devices())"

# Verificar que el microfono default funciona
arecord -d 3 test.wav && aplay test.wav
```

### Ollama no responde o está lento

```bash
# Verificar que Ollama está corriendo
curl http://localhost:11434/api/tags

# Si no, iniciarlo:
ollama serve
```

---

## 8. Del Simulador al Hardware Real

Cuando estés listo para probar en el robot físico:

### 8.1 Cambios necesarios

El único archivo que cambia es el controlador. Las herramientas de IA permanecen igual:

```
SIMULACIÓN:                       HARDWARE REAL:
sim_robot_controller.py    →     robot_voice_controller.py
     │                                  │
     │ (usa SimRobotBridge)             │ (usa WebRTC)
     │                                  │
     ▼                                  ▼
  CycloneDDS → MuJoCo              WebRTC → Go2 AIR
```

### 8.2 Pasos para migrar

1. Conectarse al WiFi del robot (`Unitree_Go2_XXXX`)
2. Verificar conectividad: `ping 192.168.12.1`
3. Ejecutar el controlador real:
   ```bash
   cd ~/proyectoProspectiva/proyecto-final
   python3 robot_voice_controller.py
   ```

### 8.3 Lo que NO cambia

- `robot_tools.py` → idéntico
- Whisper → idéntico
- Ollama + prompts → idéntico
- Guardrails → idéntico
- Comandos de voz → idéntico

---

## 9. Roadmap: Navegación Autónoma

Con la simulación funcionando, los siguientes pasos son:

### Fase 2: SLAM + Navegación (Nav2 en simulación)
- Integrar SLAM Toolbox o Cartographer para mapear el entorno
- Configurar AMCL para localización
- Usar Nav2 Planner para planificación de rutas
- Evasión de obstáculos con Costmap2D

### Fase 3: Marcadores Semánticos
- Asociar etiquetas a coordenadas del mapa ("cafetería" → x,y,z)
- Persistir el mapa semántico en YAML/JSON

### Fase 4: Wake Word + STT Continuo
- "oye amigo" como palabra de activación (Porcupine / snowboy / Vosk)
- Escucha continua sin necesidad de presionar ENTER

### Fase 5: Orquestador LLM (Qwen 0.6B)
- Function Calling: `Maps_to("cafeteria")`
- Traducir etiqueta semántica → coordenada de navegación
- Enviar goal pose a Nav2

### Fase 6: Hardware Real
- Mismo pipeline, con el robot físico
- Puente WebRTC para telemetría
- Pruebas en entorno escolar

---

## Resumen Rápido

```bash
# Terminal 1: Simulador
source /opt/ros/humble/setup.bash
~/unitree_ws/build/unitree_mujoco/unitree_mujoco

# Terminal 2: Control por voz
cd ~/proyectoProspectiva/ROS2-SIM
python3 sim_robot_controller.py

# Di tu comando, presiona ENTER, y mira el robot moverse en MuJoCo
```
