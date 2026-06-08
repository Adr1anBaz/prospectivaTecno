# ROS2-SIM — Simulacion MuJoCo + ROS 2 para Unitree Go2 AIR

Este directorio contiene todo lo necesario para probar el pipeline
de control por voz en simulacion antes de desplegar en el robot real.

## Archivos

| Archivo | Proposito |
|--------|-----------|
| `SIMULATION_SETUP.md` | Guia tecnica detallada de configuracion del entorno |
| `GUIA_SIMULACION.md` | Guia paso a paso para ejecutar y probar |
| `setup_sim.sh` | Script autonomo de instalacion (ejecutar una vez) |
| `sim_robot_controller.py` | Controlador de voz para simulacion |
| `test_sim_connection.py` | Prueba directa de comandos (sin voz) |
| `config/cyclonedds.xml` | Configuracion CycloneDDS |
| `patches/` | Parches aplicados al codigo upstream |

## Inicio Rapido

```bash
# 1. Configurar el entorno (una sola vez)
./setup_sim.sh

# 2. Terminal 1: Iniciar simulador
source /opt/ros/humble/setup.bash
~/unitree_ws/build/unitree_mujoco/unitree_mujoco

# 3. Terminal 2: Probar conexion
python3 test_sim_connection.py move 0.3 0 0

# 4. Terminal 2: Control por voz
python3 sim_robot_controller.py
```

## Arquitectura

```
Voz → Whisper (STT) → Ollama (LLM) → Tool Call JSON
                                          │
                    ┌─────────────────────┘
                    ▼
              robot_tools.py  (validacion + guardrails)
                    │
                    ▼
         ┌─────────────────────────┐
         │    CAPA DE TRANSPORTE   │
         │                         │
         │  Sim:  CycloneDDS       │
         │  Real: WebRTC           │
         └─────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────┐
         │    ROBOT / SIMULADOR    │
         │                         │
         │  Sim:  MuJoCo Go2 AIR   │
         │  Real: Unitree Go2 AIR  │
         └─────────────────────────┘
```
