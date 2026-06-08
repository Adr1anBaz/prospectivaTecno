# 🤖 Control por Voz de Robot Unitree Go2

Sistema de control por voz que permite comandar un robot Unitree Go2 mediante lenguaje natural, procesado completamente de forma local sin APIs externas.

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.9+
- macOS (probado en Darwin 24.6.0)
- Micrófono funcional
- Acceso a WiFi del robot Unitree Go2

### 1. Instalar Dependencias

```bash
# Clonar/acceder al repositorio
cd proyecto-final

# Instalar uv (gestor de paquetes Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sincronizar todas las dependencias Python
uv sync
```

### 2. Configurar Ollama (LLM Local)

```bash
# Instalar Ollama (si no está instalado)
brew install ollama

# Iniciar servicio
brew services start ollama

# Descargar modelo (1.9GB)
ollama pull qwen2.5:3b
```

### 3. Verificar Instalación

```bash
# Probar conexión al robot (conecta primero a WiFi Unitree_XXXXX)
uv run python test_connection.py
```

---

## 📚 Bibliotecas Principales

### Procesamiento de Audio y Voz

- **`openai-whisper`** (>=20231117)  
  Motor de transcripción de voz a texto. Usa el modelo `base` (~1GB) que ofrece un balance óptimo entre velocidad y precisión para comandos de voz.

- **`sounddevice`** (>=0.4.6)  
  Captura de audio desde el micrófono en tiempo real. Permite control manual de inicio/fin de grabación.

### Procesamiento Numérico

- **`torch`** (>=2.0.0)  
  Framework de deep learning requerido por Whisper. Maneja la inferencia del modelo de transcripción.

- **`numpy`** (>=1.24.0) y **`scipy`** (>=1.10.0)  
  Procesamiento de arrays de audio y operaciones matemáticas para señales digitales.

### Inteligencia Artificial Local

- **`ollama`** (>=0.4.0)  
  Cliente Python para interactuar con modelos LLM locales. Usa `qwen2.5:3b` con soporte para tool calling, que traduce lenguaje natural a comandos JSON estructurados.

### Control del Robot

- **`unitree-webrtc-connect`** (>=0.1.0)  
  Biblioteca propietaria de Unitree para establecer conexión WebRTC con el robot Go2. Permite envío de comandos de movimiento, modos de operación y gestos en tiempo real.

---

## 🎮 Uso del Sistema

### Modo Normal (con Robot)

```bash
# 1. Conectarse a la WiFi del robot
#    Red: Unitree_XXXXX

# 2. Verificar conexión
uv run python test_connection.py

# 3. Iniciar sistema de control
uv run python robot_voice_controller.py
```

**Controles:**
- **ENTER** → Iniciar/detener grabación
- **Q + ENTER** → Salir

**Comandos de voz disponibles:**
- 🏃 Movimientos: "camina adelante", "muévete a la izquierda"
- 🔄 Giros: "gira a la derecha"
- 🎭 Gestos: "siéntate", "ponte de pie", "saluda", "baila"
- ⚙️ Modos: "modo normal", "apaga los motores"

### Modo Simulación (sin Robot)

Si no tienes acceso al robot físico:

```bash
uv run python voice_to_robot.py
```

Este modo te permite probar el pipeline completo:
1. 🎤 Captura de voz
2. 📝 Transcripción con Whisper
3. 🤖 Generación de comandos con LLM
4. 🛡️ Validación con guardrails
5. ✅ Simulación de ejecución

---

## 📁 Estructura del Proyecto

```
proyecto-final/
├── robot_voice_controller.py    # ⭐ Sistema principal de control
├── test_connection.py            # 🔧 Script de diagnóstico
├── robot_tools.py                # 🛠️  Definición de tools y guardrails
├── voice_to_robot.py             # 🧪 Demo sin robot (simulación)
├── tests/                        # 📝 Tests unitarios
├── docs/                         # 📚 Documentación detallada
├── pyproject.toml                # 🔧 Configuración de dependencias
└── README.md                     # 📖 Este archivo
```

---

## 🔧 Solución de Problemas

### ❌ "Robot is not exposing a signaling port"

**Causas comunes:**
1. Robot no completamente iniciado → Espera 60s después del pitido
2. Método de conexión incorrecto → Ejecuta `test_connection.py`
3. IP incorrecta → Verifica con el dueño del robot

**Solución:**
```bash
uv run python test_connection.py
```

### ⚠️ "VIRTUAL_ENV does not match"

```bash
unset VIRTUAL_ENV
uv run python robot_voice_controller.py
```

### 🎤 Micrófono no funciona

- Ve a: **Configuración → Privacidad → Micrófono**
- Permite acceso a Terminal o tu IDE

### 🤖 Robot no responde

1. Di primero: "modo normal"
2. Asegúrate de que esté de pie
3. Reinicia la conexión (Ctrl+C y volver a ejecutar)

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│  Micrófono  │────▶│   Whisper    │────▶│   Ollama    │────▶│  Robot   │
│  (Usuario)  │     │ (Transcribe) │     │ (Tool Call) │     │  Unitree │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
                                                │
                                                ▼
                                          ┌──────────┐
                                          │Guardrails│
                                          │(Valida)  │
                                          └──────────┘
```

**Flujo de procesamiento:**
1. Usuario presiona ENTER y habla comando
2. `sounddevice` captura audio en tiempo real
3. `Whisper` transcribe audio a texto
4. `Ollama` (Qwen2.5) genera comando JSON estructurado
5. Sistema de guardrails valida seguridad
6. `unitree-webrtc-connect` envía comando al robot
7. Robot ejecuta acción y devuelve estado

---

## ⚙️ Especificaciones Técnicas

**Modelos de IA:**
- Whisper: `base` (~1GB)
- LLM: `qwen2.5:3b` (~1.9GB)

**Hardware:**
- Robot: Unitree Go2
- Protocolo: WebRTC
- Red: LocalAP (192.168.12.x)

**Sistema de Guardrails:**
- Validación de parámetros numéricos
- Prevención de comandos peligrosos
- Límites de velocidad y distancia
- Detección de comandos ambiguos
- Log de comandos ejecutados

---

## 📚 Documentación Adicional

Para más detalles, consulta la carpeta `docs/`:
- **GUIA_RAPIDA.md** - Guía de uso detallada
- **GUIA_CONEXION_ROBOT.md** - Troubleshooting de conexión
- **FLUJO_COMPLETO.md** - Diagramas de flujo

---

## 🤝 Contribuir

Este proyecto fue desarrollado como prueba de concepto para control robótico mediante voz usando únicamente recursos locales (sin APIs externas).

**Características destacadas:**
- ✅ 100% local (sin internet en tiempo de ejecución)
- ✅ Control manual y seguro de grabación
- ✅ Arquitectura modular y extensible
- ✅ Sistema de seguridad multi-capa
- ✅ Manejo robusto de errores
