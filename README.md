# Asistente de Voz Universitario — Blu

Asistente de navegación e información para campus universitario con reconocimiento de voz local, wake word offline, múltiples proveedores de STT/TTS/LLM, e integración con servidor MCP y Route API.

> Rama activa de desarrollo: `main`

---

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) para manejo de dependencias
- API keys (según proveedores que uses):
  - **Groq** (`GROQ_API_KEY`): https://console.groq.com
  - **Deepgram** (`DEEPGRAM_API_KEY`): https://developers.deepgram.com
  - **OpenRouter** (`OPENROUTER_API_KEY`, opcional): https://openrouter.ai
- **Parakeet STT local** (opcional): requiere el modelo ONNX descargado por la app Handy (ver sección [Modelo Parakeet](#modelo-parakeet-stt-local))
- (Opcional) Cuenta de Google Cloud con **Cloud Speech-to-Text API** habilitada

---

## Instalación

```bash
# 1. Clonar la rama main
git clone -b main https://github.com/Adr1anBaz/prospectivaTecno.git
cd prospectivaTecno

# 2. Crear .env a partir del ejemplo
cp .env.example .env

# 3. Editar .env con tus API keys y proveedores deseados
#    GROQ_API_KEY=...
#    DEEPGRAM_API_KEY=...

# 4. Instalar dependencias
uv sync
```

### Modelo de wake word (solo modo audio)

El modo audio usa Vosk para detectar la palabra clave `"ronaldo"`. Descarga el modelo:

```bash
uv run python scripts/download_vosk_model.py
```

> Si solo usarás el **modo texto** (`--text`), no necesitas el modelo Vosk.

### Modelo Parakeet STT (local, opcional)

Para usar el proveedor `parakeet` (STT 100% local sin conexión a internet), necesitas el modelo ONNX de NVIDIA NeMo Parakeet-TDT que la app Handy descarga automáticamente. El asistente lo usa en modo solo lectura (no modifica los archivos de Handy).

**Si tienes Handy instalado**, el modelo ya está en:

```
~/.local/share/com.pais.handy/models/parakeet-tdt-0.6b-v3-int8/
```

Debe contener estos 4 archivos:

| Archivo | Rol |
|---|---|
| `nemo128.onnx` | Preprocesador acústico (waveform → features) |
| `encoder-model.int8.onnx` | Encoder acústico |
| `decoder_joint-model.int8.onnx` | Decoder Transducer (RNNT greedy) |
| `vocab.txt` | Vocabulario de 8193 tokens (blank=8192) |

**Si no tienes Handy**, descarga el modelo manualmente:

```bash
# Crear el directorio
mkdir -p ~/.local/share/com.pais.handy/models/

# Descargar desde Hugging Face (NVIDIA NeMo)
# Parakeet-TDT 0.6B (int8 quantized)
wget -P ~/.local/share/com.pais.handy/models/parakeet-tdt-0.6b-v3-int8/ \
  https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3-int8/resolve/main/nemo128.onnx \
  https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3-int8/resolve/main/encoder-model.int8.onnx \
  https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3-int8/resolve/main/decoder_joint-model.int8.onnx \
  https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3-int8/resolve/main/vocab.txt
```

Luego en `.env`:

```bash
STT_PROVIDER=parakeet
PARAKEET_MODEL_DIR=/home/rimuru/.local/share/com.pais.handy/models/parakeet-tdt-0.6b-v3-int8
```

> **Nota:** La primera transcripción carga los 3 modelos ONNX (~2-3s). Las siguientes son rápidas porque las sesiones se reutilizan. Si tienes GPU NVIDIA, automáticamente usará `CUDAExecutionProvider`.

---

## Modo de ejecución

### Modo audio (normal)

Usa el micrófono. Di `"ronaldo"` seguido del comando.

```bash
# Con servidores reales (MCP + Route)
uv run python src/prospectiva/main.py

# Con clientes mock (no requiere servidores externos)
uv run python src/prospectiva/main.py --test
```

### Modo texto (para pruebas sin micrófono)

Escribe los comandos en lugar de hablarlos. Útil para probar todas las funcionalidades sin depender del micrófono ni de STT.

```bash
uv run python src/prospectiva/main.py --text --test
```

#### Cómo usar el modo texto

| Entrada | Qué hace |
|---------|----------|
| `ronaldo llévame a biomédica` | Simula wake word + comando de navegación |
| `ronaldo qué hay en la cafetería` | Pregunta conversacional (usa LLM + tools MCP) |
| `gracias` | Respuesta directa cuando estás en modo conversación |
| `/wake` | Fuerza manualmente el estado de escucha |
| `/end` | Termina el modo conversación |
| `/exit` o `exit` | Cierra el asistente |

#### Ejemplo de sesión en modo texto

```
🎤 [ronaldo] > ronaldo llévame a biomédica
🤖 ACCIÓN EJECUTADA
  • Comando: 'llévame a biomédica'
  • Intent detectado: NAVEGAR_BIOMEDICA
  ...

🎤 [ronaldo] > ronaldo qué comida hay en la cafetería
🧠 RESPUESTA CONVERSACIONAL
  ...

🗣️  > gracias
🧠 RESPUESTA CONVERSACIONAL
  ...

🗣️  > /end
🔇 Modo conversación terminado.

🎤 [ronaldo] > /exit
👋 Saliendo...
```

---

## Proveedores

### STT (Speech-to-Text)

| Proveedor | Modo | Descripción | API Key |
|---|---|---|---|
| `groq` (default) | Online | Whisper large-v3-turbo, rápido y preciso | `GROQ_API_KEY` |
| `deepgram` | Online | Nova-3 streaming, baja latencia | `DEEPGRAM_API_KEY` |
| `googlecloud` | Online | Google Cloud Speech-to-Text | Service Account JSON |
| `parakeet` | **Local** | ONNX Parakeet-TDT, sin conexión, requiere GPU recomendada | No necesita |

En `.env`:

```bash
STT_PROVIDER=parakeet
```

### TTS (Text-to-Speech)

| Proveedor | Streaming | Descripción | API Key |
|---|---|---|---|
| `edge` (default) | ✅ Sí | Microsoft Edge TTS, rápido, gratuito, muchas voces | No necesita |
| `deepgram` | ✅ Sí | Deepgram Aura-2, voces naturales | `DEEPGRAM_API_KEY` |
| `local` | ❌ No | Mock offline para pruebas | No necesita |

En `.env`:

```bash
TTS_PROVIDER=edge
TTS_MODEL=es-MX-JorgeNeural
```

Voces Edge disponibles en español:
- `es-MX-JorgeNeural` (masculino, default)
- `es-MX-DaliaNeural` (femenino)

Voces Deepgram Aura-2:
- `aura-2-celeste-es`, `aura-2-alejandra-es`, `aura-2-sofia-es` (femenino)
- `aura-2-marcos-es`, `aura-2-octavio-es` (masculino)

### LLM

| Proveedor | Descripción |
|---|---|
| `groq` (default) | Llama 4 Scout 17B, rápida, gratis |
| `openrouter` | OpenRouter con fallback a Groq si falla |

En `.env`:

```bash
LLM_PROVIDER=groq
LLM_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
```

---

## Anti-feedback (bucle de audio)

El asistente incorpora un sistema anti-feedback para evitar que el micrófono capture la voz del TTS y entre en un bucle infinito:

| Mecanismo | Descripción |
|---|---|
| **Muteo durante TTS** | Ignora chunks de micrófono mientras `AUDIO_STREAM_START` está activo |
| **Cooldown adaptativo post-TTS** | Después de que el TTS termina, espera `max(3s, duración_TTS × 1.5)` antes de escuchar de nuevo (máx 8s). El eco/rebote de la bocina se disipa en ese tiempo |
| **VAD streak** | En modo conversación, requiere 3 chunks consecutivos de VAD positivo antes de empezar a capturar. Filtra ruido ambiente y picos aislados |
| **Flush de buffer en inicio de TTS** | Cuando el TTS empieza a reproducirse, se descarta cualquier audio capturado justo antes |
| **Fin de conversación por tool resolutiva** | Si el LLM llamó `navigate_to`, `list_places`, etc., la conversación termina automáticamente (no se queda escuchando después de navegar) |
| **Fin de conversación por transcripción vacía** | Si Parakeet devuelve texto vacío (silencio/ruido), se publica `CONVERSATION_END` para romper el bucle |

Configuración en `.env`:

```bash
# Milisegundos de cooldown mínimo después del TTS (default: 3000)
POST_TTS_COOLDOWN_MS=3000
```

---

## Servidores externos (MCP + Route)

Este repositorio contiene únicamente el **asistente**. Los datos del campus y el cálculo de rutas viven en el repositorio companion [`mcp-blu`](https://github.com/Adr1anBaz/mcp-blu).

### 1. Clonar y levantar `mcp-blu`

```bash
git clone https://github.com/Adr1anBaz/mcp-blu.git
cd mcp-blu

# Configurar variables de entorno (mismo token en ambos .env)
cp .env.example .env
cp mcp-server/.env.example mcp-server/.env

# Levantar PostgreSQL con datos de ejemplo
docker compose up -d
```

### 2. Iniciar MCP server (terminal 1)

```bash
cd mcp-blu/mcp-server
uv run server.py
# -> http://localhost:8000/mcp
```

### 3. Iniciar Route server (terminal 2)

```bash
cd mcp-blu
uv run route_server.py
# -> http://localhost:8001
```

### 4. Configurar el asistente

En el `.env` de `prospectivaTecno` asegúrate de que apunten a los servidores anteriores:

```bash
MCP_URL=http://localhost:8000/mcp
MCP_BEARER_TOKEN=el-mismo-token-de-mcp-blu
ROUTE_API_URL=http://localhost:8001
```

### 5. Iniciar el asistente (terminal 3)

```bash
cd prospectivaTecno
uv run python src/prospectiva/main.py --text
```

> El asistente en modo `--test` usa clientes mock y no requiere los servidores externos.

---

## Funcionalidades principales

- **Wake word**: `"ronaldo"` detectada offline con Vosk (coincidencias parciales permitidas para respuesta rápida)
- **STT local**: Parakeet-TDT 0.6B (ONNX, NVIDIA NeMo), sin conexión a internet
- **STT online**: Groq Whisper, Deepgram Nova-3, Google Cloud Speech-to-Text
- **TTS streaming**: Edge TTS (gratuito) o Deepgram Aura-2, reproducción chunk-by-chunk
- **LLM**: Groq Llama 4 + fallback OpenRouter si Groq falla
- **Tool calling nativo**: 12 herramientas MCP (search_places, navigate_to, search_food, etc.)
- **Navegación**: comandos directos a edificios del campus con cálculo de ruta
- **Robot**: comandos de movimiento (`siéntate`, `baila`, `camina`, `detente`, etc.)
- **Conversación**: modo que mantiene escucha activa sin repetir wake word
- **Anti-feedback**: cooldown adaptativo + VAD streak + flush de buffer en TTS
- **Modo texto**: prueba todo sin micrófono, útil para desarrollo

---

## Arquitectura

```
src/prospectiva/
├── main.py                 # Punto de entrada, factory de providers, lanza procesos
├── bus/
│   └── event_bus.py        # Bus de eventos entre procesos (multiprocessing)
├── modulos/
│   ├── llm/                # GroqLLM, OpenRouterLLM, FallbackLLM
│   ├── stt/                # GroqSTT, DeepgramSTT, GoogleCloudSTT, ParakeetSTT
│   ├── tts/                # DeepgramTTS, EdgeTTS, LocalTTS
│   ├── muta/               # SoundDeviceAudio, SileroVAD, VoskWakeWord, PorcupineWakeWord
│   └── classifier/         # Clasificador de intents (YAML config)
├── procesos/
│   ├── audio.py            # Proceso de audio: wake word → VAD → SPEECH_COMPLETED
│   ├── text_input.py       # Modo texto (stdin)
│   ├── orquestador.py      # Orquestador central: STT → LLM → tools → TTS
│   ├── playback.py         # Reproducción de audio TTS streaming
│   └── movement.py         # Ejecución de movimientos (archivos CSV de ruta)
└── utils/
    ├── mcp_client.py       # Cliente JSON-RPC para MCP server (puerto 8000)
    ├── route_client.py     # Cliente REST para Route server (puerto 8001/8081)
    ├── memory.py           # Memoria de conversación (multi-turno)
    ├── tool_tracker.py     # Tracker de uso de herramientas MCP
    └── mock_*.py           # Mock clients para modo --test
```

### Flujo de datos

```
Micrófono → VAD → Buffer → SPEECH_COMPLETED
                                ↓
[AudioProcess]              [Orquestador]
                                ↓
                           ParakeetSTT / GroqSTT / etc.
                                ↓
                           Classifier (intent)
                           ├── NAVEGAR_*/COMANDO_* → acción directa + movimiento
                           └── HABLAR → LLM + tool calling MCP
                                ↓
                           EdgeTTS / DeepgramTTS (streaming)
                                ↓
[AudioPlayback]           AUDIO_STREAM_START → CHUNK → CHUNK → END
                                ↓
                           Bocina (sounddevice)
```

---

## Dependencias principales

| Paquete | Propósito |
|---|---|
| `onnxruntime` | Ejecución del modelo ONNX Parakeet (CPU/GPU) |
| `numpy` | Procesamiento de audio |
| `sounddevice` | Captura y reproducción de audio |
| `silero-vad` | Detección de actividad de voz |
| `vosk` | Wake word offline |
| `pvporcupine` | Wake word alternativa (Picovoice) |
| `scipy` | Resample de audio (fallback si no hay torchaudio) |
| `groq` | Cliente Groq API (LLM + Whisper STT) |
| `deepgram-sdk` | Cliente Deepgram API (STT + TTS) |
| `edge-tts` | TTS gratuito con Microsoft Edge |
| `httpx` | Cliente HTTP para MCP/Route API |
| `python-dotenv` | Carga de variables de entorno |
| `mcp` | SDK de Model Context Protocol |
| `google-cloud-speech` | Google Cloud STT (opcional) |
| `pydub` | Utilidades de audio |

---

## Notas técnicas

- El proyecto usa **multiprocessing** con `spawn` (modo audio) o `fork` (modo texto).
- El modo `--test` usa clientes MCP y Route mock para pruebas sin levantar servidores.
- La carpeta `credentials/` está ignorada en git para proteger las claves de Google Cloud.
- El `.env` tiene prioridad sobre variables de entorno del sistema (`load_dotenv(override=True)`).
- La decodificación del modelo Parakeet usa RNNT greedy con state caching (no beam search).
- El audio se captura en int16 a 16kHz y se convierte a float32 dividiendo por 32768 (sin normalización adicional).
