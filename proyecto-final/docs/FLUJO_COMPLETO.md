# 🔄 Flujo Completo del Sistema

## Diagrama del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    INICIO DEL SISTEMA                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  1. ENCENDER ROBOT                                          │
│     • Presionar botón físico                                │
│     • Esperar pitido (~30 seg)                              │
│     • Robot en posición inicial                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. CONECTAR WIFI                                           │
│     • WiFi: Unitree_XXXXX                                   │
│     • IP: 192.168.12.1                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  3. EJECUTAR SCRIPT                                         │
│     $ uv run python robot_voice_controller.py               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  4. CONEXIÓN WEBRTC                                         │
│     • Establecer canal de comunicación                      │
│     • Verificar estado del robot                            │
│     ✅ Conexión establecida                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  5. CARGAR MODELOS                                          │
│     • Whisper (base) - 1GB                                  │
│     • Ollama (qwen2.5:3b) - 1.9GB                           │
│     ✅ Modelos cargados                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ╔═══════════════════════════════════════════╗
        ║                                           ║
        ║         LOOP INFINITO (Ctrl+C para salir) ║
        ║                                           ║
        ╚═══════════════════════════════════════════╝
                            │
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  ESTADO: IDLE (Esperando)                                   │
│  ✅ LISTO PARA ESCUCHAR (Comando #N)                        │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  ESTADO: LISTENING (Escuchando)                             │
│  ⏺️ 🔴 GRABANDO... (presiona ENTER para DETENER)            │
│                                                             │
│  [Grabación de audio con micrófono]                        │
│  • Sample rate: 16000 Hz                                   │
│  • Duración: Controlada por usuario (ENTER para detener)  │
│  • Formato: Float32, Mono                                  │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  ESTADO: PROCESSING (Procesando)                            │
│  📝 Transcribiendo...                                       │
│                                                             │
│  [Whisper: Audio → Texto]                                  │
│  Input:  Audio array (numpy)                               │
│  Output: "camina hacia adelante"                           │
│  💬 Comando: "camina hacia adelante"                        │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  ESTADO: PROCESSING (Generando comando)                     │
│  🤖 Generando comando para el robot...                      │
│                                                             │
│  [Ollama: Texto → Tool Call JSON]                          │
│  • Model: qwen2.5:3b                                       │
│  • System Prompt + Few-Shot Examples                       │
│  • Temperature: 0.0 (determinista)                         │
│  • Format: JSON                                            │
│                                                             │
│  Output: {"name": "move_robot",                            │
│           "arguments": {"x": 0.3, "y": 0, "z": 0}}         │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  POST-PROCESAMIENTO                                         │
│  • Detectar comando simple vs compuesto                    │
│  • Corregir polaridad si es necesario                      │
│  • Validar contra guardrails                               │
│  📋 Tool call: {"name": "move_robot", ...}                 │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  VALIDACIÓN DE GUARDRAILS                                   │
│  🛡️ Verificando seguridad...                               │
│                                                             │
│  Checks:                                                    │
│  ✓ x en rango [-0.5, 0.5]                                  │
│  ✓ y en rango [-0.5, 0.5]                                  │
│  ✓ z en rango [-1.0, 1.0]                                  │
│  ✓ action_name en whitelist                                │
│  ✓ mode_name en whitelist                                  │
│                                                             │
│  ✅ Comando seguro y válido                                 │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  ESTADO: EXECUTING (Ejecutando)                             │
│  🤖 EJECUTANDO: move_robot                                  │
│  📊 Parámetros: {"x": 0.3, "y": 0.0, "z": 0.0}             │
│                                                             │
│  [Envío a Robot via WebRTC]                                │
│  • Publicar comando en RTC_TOPIC["SPORT_MOD"]              │
│  • API: SPORT_CMD["Move"]                                  │
│  • Duración: 2.0 segundos                                  │
│  • Auto-detener después                                    │
│                                                             │
│  🔒 BLOQUEADO - No acepta nuevos comandos                   │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  ROBOT EJECUTA MOVIMIENTO                                   │
│  🐕 Robot moviéndose...                                     │
│  • x=0.3 → Avanza                                          │
│  • Duración: 2 segundos                                    │
│  • Sistema espera finalización                             │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  AUTO-DETENER                                               │
│  🛑 Enviando comando de parada...                           │
│  • x=0, y=0, z=0                                           │
│  • Estabilización: 0.5 seg                                 │
│  ✅ Comando completado                                      │
└─────────────────────────────────────────────────────────────┘
                │                       │
                ▼                       │
┌─────────────────────────────────────────────────────────────┐
│  CAMBIO DE ESTADO                                           │
│  is_executing = False                                       │
│  state = IDLE                                               │
│  Pausa: 1 segundo                                           │
└─────────────────────────────────────────────────────────────┘
                │                       │
                └───────────────────────┘
                         (Repite)


        ╔═══════════════════════════════════════════╗
        ║          SALIR DEL SISTEMA (Ctrl+C)       ║
        ╚═══════════════════════════════════════════╝
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  SHUTDOWN SEGURO                                            │
│  🛑 Deteniendo sistema...                                   │
│                                                             │
│  1. Enviar comando de parada (x=0, y=0, z=0)               │
│  2. Esperar estabilización (0.5 seg)                       │
│  3. Cerrar conexión WebRTC                                 │
│  4. Liberar recursos                                       │
│                                                             │
│  ✅ Sistema cerrado correctamente                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    FIN DEL SISTEMA                          │
│            👋 Programa terminado                            │
└─────────────────────────────────────────────────────────────┘
```

---

## ⏱️ Tiempos de Procesamiento (Aproximados)

```
Grabación de audio:          Controlada por usuario (presionar ENTER para detener)
Transcripción (Whisper):     2-3 segundos (depende de duración del audio)
Generación tool call (LLM):  1-2 segundos
Validación:                  <0.1 segundos
Ejecución en robot:          Variable según comando:
  • Movimiento simple:       2.0 segundos
  • Animación:               3.0 segundos
  • Cambio de modo:          3.0 segundos
Estabilización:              0.5-1.0 segundos

TOTAL por comando:           ~6-15 segundos (+ tiempo de grabación)
```

---

## 🔄 Estados del Sistema

```
DISCONNECTED → No conectado al robot
     ↓
IDLE         → Esperando comando (puede recibir nuevos comandos)
     ↓
LISTENING    → Grabando audio del micrófono
     ↓
PROCESSING   → Transcribiendo y generando tool call
     ↓
EXECUTING    → Ejecutando comando en robot (BLOQUEADO)
     ↓
IDLE         → Vuelve a esperar
```

**Nota importante:** Solo en estado `IDLE` se aceptan nuevos comandos.

---

## 🔐 Capas de Seguridad

```
Comando de Voz
      ↓
[1] Transcripción → Whisper valida audio
      ↓
[2] LLM Generation → Ollama + Few-shot examples
      ↓
[3] Post-Processing → Corrige errores comunes
      ↓
[4] Guardrails → Valida rangos y whitelists
      ↓
[5] Execution Lock → Solo un comando a la vez
      ↓
Robot (Comando Seguro)
```

---

## 📊 Ejemplo de Logs Completos

```
============================================================
🤖 CONECTANDO AL ROBOT UNITREE
============================================================
📡 IP: 192.168.12.1
✅ Conexión WebRTC establecida

⏳ Cargando Whisper 'base'...
✅ Whisper cargado

============================================================
🎙️  SISTEMA DE CONTROL POR VOZ ACTIVO
============================================================
Modelo LLM: qwen2.5:3b
Modelo Whisper: base

💡 Comandos de voz disponibles:
   • Movimiento: 'camina adelante', 'gira a la derecha'
   • Animaciones: 'siéntate', 'saluda', 'baila'
   • Modos: 'modo normal', 'apaga motores'
   • Control: 'detente', 'para'

⌨️  Control del sistema:
   • ENTER → Activar micrófono (inicio de grabación)
   • ENTER nuevamente → Detener grabación
   • Q + ENTER → Salir de forma segura
============================================================

============================================================
✅ LISTO PARA ESCUCHAR (Comando #1)
============================================================

⏺️ 🔴 GRABANDO... (presiona ENTER para DETENER)

⏹️  Grabación detenida (X.X segundos)

📝 Transcribiendo...
💬 Comando: "camina hacia adelante"
🤖 Generando comando para el robot...
📋 Tool call: {"name": "move_robot", "arguments": {"x": 0.3, "y": 0.0, "z": 0.0}}

🤖 EJECUTANDO: move_robot
📊 Parámetros: {
  "x": 0.3,
  "y": 0.0,
  "z": 0.0
}
✅ Comando completado

============================================================
✅ LISTO PARA ESCUCHAR (Comando #2)
============================================================
```

---

## 🎯 Resumen del Flujo

1. **Inicio**: Conectar → Cargar modelos
2. **Loop**: Escuchar → Procesar → Validar → Ejecutar
3. **Bloqueo**: Solo un comando a la vez
4. **Seguridad**: 5 capas de validación
5. **Shutdown**: Detener robot → Cerrar conexión

**Duración típica por comando:** 10-15 segundos
**Comandos por minuto:** ~4-6
**Estado crítico:** `EXECUTING` (bloqueado)
