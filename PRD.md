***
# Documento de Requisitos del Producto (PRD) - v2.0
## Asistente de Voz Universitario en Español - Baja Latencia y Alta Resiliencia (Edge/Cloud)

### 1. Visión General del Proyecto
Sistema de asistencia por voz modular y de latencia ultrabaja para un robot/dispositivo de navegación en un entorno universitario. El sistema procesa comandos de navegación y responde preguntas de manera conversacional, **totalmente en español**.

**Restricción Crítica:** El sistema opera en entornos con conectividad inestable. Requiere una arquitectura de "Degradación Elegante" (Graceful Degradation), priorizando APIs en la nube (Groq/Deepgram) cuando hay red, y conmutando automáticamente a modelos locales (faster-whisper/llama.cpp/Piper TTS) en una Raspberry Pi 5 (8GB) cuando la red falla, garantizando que los comandos críticos de navegación nunca se detengan.

**Wake Word:** "Oye Robot" (Español) — usando Porcupine (Picovoice) en lugar de openWakeWord, que solo soporta inglés.

**Gestor de Entorno:** `uv` (v0.11+) para creación del venv, instalación de dependencias y gestión del proyecto.

---

### 2. Stack Tecnológico Definitivo (Verificado Junio 2026)

| Módulo | Cloud (Online) | Local/Edge (Offline - RP5) |
|---|---|---|
| **Wake Word** | — | Porcupine (Picovoice) v4.0.2 — "Oye Robot", español, 100% on-device |
| **VAD (Voice Activity Detection)** | — | Silero VAD v6.2.1 — ONNX, producción-estable |
| **STT (Speech-to-Text)** | Groq API: whisper-large-v3-turbo ($0.04/hr) | faster-whisper (CTranslate2) — modelo tiny o base, INT8 quantization |
| **Clasificador de Intención** | — | Regex/Rules para PoC (Fase 2-3). Evaluar ONNX optimization del cross-encoder/nli-distilroberta-base para Fase 4 |
| **LLM (Generación de Texto)** | Groq API: llama-3.1-8b-instant (560 T/s, $0.05/M tok input) | llama-cpp-python v0.3.20 + Qwen2.5-0.5B-Instruct GGUF Q4_K_M |
| **TTS (Text-to-Speech)** | Deepgram Aura-2 (modelo aura-2-thalia-en, voz español disponible) | piper-tts v1.4.2 — voz es_ES-davefx-medium (65MB, 22kHz, español) |
| **Audio I/O** | — | sounddevice v0.5.5 (bindings PortAudio, NumPy nativo, wheels ARM64) |
| **Concurrencia** | — | multiprocessing, asyncio, queue.Queue |
| **Gestor Proyecto** | — | UV v0.11.19 |

#### 2.1. Modelos Cloud (Groq) - Detalles Específicos
- **STT:** `whisper-large-v3-turbo` — 228x real-time, 99+ idiomas, $0.04/hr. NO usar `whisper-large-v3` (más caro: $0.111/hr).
- **LLM:** `llama-3.1-8b-instant` — contexto 131K tokens, 560 tokens/seg. NO usar el ID `llama-3-8b-8192` (obsoleto).
- **SDK:** `groq` >=1.3.0, Python >=3.10, cliente sincrono y asíncrono vía httpx.

#### 2.2. Audiostream - sounddevice
- Usar `sounddevice` en vez de `pyaudio`. Razones: API más limpia, trabaja directamente con NumPy arrays, mantenimiento activo (v0.5.5, Ene 2026), wheels oficiales para ARM64.
- Dependencia sistema Linux: `libportaudio2`, `portaudio19-dev`.

#### 2.3. Wake Word - Porcupine (reemplaza openWakeWord)
- openWakeWord (v0.6.0) solo soporta wake words en inglés. No viable para asistente en español.
- Porcupine soporta español como idioma nativo, corre 100% on-device en Raspberry Pi 5, requiere un AccessKey gratuito de Picovoice Console.
- La wake word elegida es **"Oye Robot"**, el modelo `.ppn` se genera desde Picovoice Console seleccionando plataforma "Raspberry Pi".
- SDK Python: `pvporcupine` v4.0.2 (PyPI activo, compatible Python >=3.9).

#### 2.4. STT Local - faster-whisper (reemplaza whisper.cpp)
- whisper.cpp es viable pero `faster-whisper` (backend CTranslate2) tiene mejor rendimiento en benchmarks 2026 para CPU ARM con INT8 quantization.
- Integración Python más limpia (API nativa, no requiere bindings C++).
- Modelos: `tiny` (~75MB) o `base` (~150MB) con `compute_type="int8"`.
- Instalación: `pip install faster-whisper`.

#### 2.5. LLM Local - llama-cpp-python + Qwen2.5-0.5B (reemplaza Qwen2)
- El modelo actual es **Qwen2.5-0.5B-Instruct**, NO Qwen2-0.5B (obsoleto).
- Cuantización recomendada: **Q4_K_M** (~400MB). Tamaño justo para RP5 8GB junto con otros modelos.
- Velocidad esperada en RP5: 5-15 tokens/segundo.
- Otras opciones viables: Phi-3-mini-3.8B Q4_K_M (~2.3GB) si se requiere más capacidad a costa de velocidad.
- Instalación: `pip install llama-cpp-python` (compila desde fuente para optimizar para la CPU local).
- Descarga del GGUF: desde HuggingFace vía `huggingface-hub` (ej. `lmstudio-community/Qwen2.5-0.5B-Instruct-GGUF`).

#### 2.6. TTS Local - piper-tts
- El paquete PyPI `piper-tts` v1.4.2 es el fork GPL-3.0 activamente mantenido (Abr 2026).
- Voz española: **es_ES-davefx-medium** (masculina, 22.05kHz, ~65MB ONNX). Alternativas: es_ES-sharvard-medium, es_MX-ald-medium, es_ES-carlfm-x_low (más ligera).
- Descarga desde HuggingFace: `rhasspy/piper-voices` o mirror `Trelis/piper-es-es-davefx-medium`.
- Síntesis en RP5: <1 segundo para frases cortas con modelo medium.
- Se puede usar vía Python (`from piper import PiperVoice`) o subprocess.

#### 2.7. TTS Cloud - Deepgram (reemplaza opción dual Deepgram/ElevenLabs)
- Deepgram Aura-2: soporta español, latencia baja, SDK Python activo (`deepgram-sdk`).
- Modelo recomendado: `aura-2-thalia-en` (voz femenina en español, entre otras disponibles).
- Máximo 2000 caracteres por request.
- Control de velocidad vía parámetro `speed` (0.7-1.5).
- ElevenLabs queda descartado por ahora (más caro, no ofrece ventajas críticas sobre Deepgram para este caso de uso).

#### 2.8. Clasificador de Intención
- **Fase 2-3:** Implementación basada en **Regex/Rules**. Solo hay 5 intents:
  - `HABLAR` — preguntas conversacionales → LLM
  - `NAVEGAR_GIORNALE` — navegar a Giornale
  - `NAVEGAR_BIOMEDICA` — navegar a Biomedica
  - `COMANDO_SIT` — comando "sentarse"
  - `COMANDO_DANCE` — comando "bailar"
- Con 5 intents bien diferenciados, Regex es suficiente, deterministico, y cumple <10ms sin esfuerzo.
- **Fase 4 (opcional):** Si se requiere mejora, evaluar el modelo `cross-encoder/nli-distilroberta-base` (82M params) exportado a ONNX con INT8 quantization. Si no cumple <10ms en RP5, mantener Regex.

---

### 3. Arquitectura del Sistema

#### 3.1. Patrón General
Python con **Arquitectura Orientada a Eventos (Event-Driven)** + **Multiprocesamiento** para evadir el GIL.

#### 3.2. Procesos (Multiprocessing)

```
┌─────────────────────────────────────────────────────┐
│                   ORQUESTADOR                        │
│  ┌─────────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ Event Bus   │ │ State    │ │ Circuit Breaker  │  │
│  │ (Queue)     │ │ Machine  │ │ (Online/Offline) │  │
│  └─────────────┘ └──────────┘ └──────────────────┘  │
└───────────────────────┬─────────────────────────────┘
                        │ eventos
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
┌─────────────────┐ ┌──────────┐ ┌──────────┐
│ AUDIO PROCESS   │ │ WORKER   │ │ WORKER   │
│ Mic/VAD/WakeWrd │ │ STT/LLM/ │ │ STT/LLM/ │
│                 │ │ TTS      │ │ TTS      │
│ sounddevice     │ │ (online) │ │ (local)  │
│ porcupine       │ │ Groq     │ │ f-whispe │
│ silero-vad      │ │ Deepgram │ │ llama.cpp│
│                 │ │          │ │ piper    │
└─────────────────┘ └──────────┘ └──────────┘
```

**Proceso de Audio (Input):**
- Bucle continuo capturando audio con `sounddevice.RawInputStream`.
- Ejecuta Porcupine para wake word "Oye Robot".
- Tras wake word, alimenta Silero VAD para detectar final de frase.
- Publica `WAKE_WORD_DETECTED` y `SPEECH_COMPLETED` (audio bytes).

**Proceso Orquestador (Core):**
- Contiene el `EventBus` (basado en `multiprocessing.Queue` + `Pipe`).
- Implementa la máquina de estados y el `CircuitBreaker`.
- Monitorea conectividad (timeout 800ms a APIs).
- Conmuta workers entre modo ONLINE y OFFLINE.
- Maneja el streaming en cascada (LLM → fragmentación → TTS simultáneo).

**Procesos Workers (Inferencia/Red):**
- Worker ONLINE: Groq STT + Groq LLM + Deepgram TTS.
- Worker OFFLINE: faster-whisper + llama.cpp/Qwen2.5 + piper-tts.
- Cada worker corre en su propio proceso con hilos internos para operaciones concurrentes.

#### 3.3. Bus de Eventos

| Evento | Payload | Emisor | Receptor(es) |
|---|---|---|---|
| `WAKE_WORD_DETECTED` | {"timestamp": float} | Audio Process | Orquestador |
| `SPEECH_COMPLETED` | {"audio": bytes, "format": str} | Audio Process | Worker STT |
| `TEXT_TRANSCRIBED` | {"text": str, "lang": str} | Worker STT | Orquestador |
| `INTENT_CLASSIFIED` | {"intent": Enum, "confidence": float, "metadata": dict} | Orquestador | Orquestador/Workers |
| `ACTION_TRIGGERED` | {"action": str, "params": dict} | Orquestador | Módulo Navegación |
| `TEXT_GENERATED` | {"text": str, "fragment": bool, "final": bool} | Worker LLM | Orquestador → Worker TTS |
| `AUDIO_SYNTHESIZED` | {"audio": bytes, "format": str} | Worker TTS | Orquestador → Audio Output |
| `STATE_CHANGED` | {"state": "ONLINE"\|"OFFLINE", "reason": str} | CircuitBreaker | Todos |
| `ERROR` | {"module": str, "error": str, "fatal": bool} | Cualquier proceso | Orquestador |

#### 3.4. Diagrama de Flujo (End-to-End)

```
USUARIO habla → [Mic] → Porcupine detecta "Oye Robot"
    → WAKE_WORD_DETECTED → [Inicia grabación con Silero VAD]
    → USUARIO termina de hablar → Silero detecta silencio
    → SPEECH_COMPLETED(audio_bytes)
    → [CircuitBreaker decide ruta]
        → ONLINE:  Groq STT (whisper-large-v3-turbo)
        → OFFLINE: faster-whisper (tiny INT8)
    → TEXT_TRANSCRIBED(texto)
    → [Clasificador Regex] determina intent
        → Si es NAVEGAR_* o COMANDO_*:
            → ACTION_TRIGGERED → [Módulo Navegación] → AUDIO_SYNTHESIZED(confirmación)
        → Si es HABLAR:
            → [CircuitBreaker decide ruta]
                → ONLINE:  Groq LLM (llama-3.1-8b-instant con system prompt)
                → OFFLINE: llama-cpp-python (Qwen2.5-0.5B Q4_K_M con system prompt)
            → TEXT_GENERATED(fragmentos)
            → [Streaming en cascada: Regex detecta .,;!? → envía fragmento a TTS inmediatamente]
                → ONLINE:  Deepgram Aura-2
                → OFFLINE: Piper TTS (es_ES-davefx-medium)
            → AUDIO_SYNTHESIZED → [Altavoz]
```

---

### 4. Especificaciones de Hardware y Entornos

| Característica | Desarrollo (Fase 1-3) | Producción (Fase 4) |
|---|---|---|
| **Plataforma** | PC Windows/Mac/Linux x86_64 | Raspberry Pi 5 (8GB RAM) |
| **SO** | Cualquiera con Python 3.10+ | Debian 12 / Ubuntu 24.04 LTS ARM64 |
| **GPU** | Opcional (no requerida) | No tiene (inferencia CPU ARM NEON) |
| **Audio** | Micrófono USB + Altavoz | Micrófono USB + Altavoz 3.5mm/USB |
| **Almacenamiento** | N/A | MicroSD 64GB+ (modelos ocupan ~1.5GB) |
| **Refrigeración** | N/A | Necesaria (ventilador activo para RP5) |
| **Red** | Ethernet/WiFi estable | WiFi (conectividad intermitente) |

#### 4.1. Budget de Memoria en RP5 (8GB)

| Componente | RAM estimada |
|---|---|
| SO + Servicios del sistema | ~500 MB |
| Porcupine (wake word) | ~50 MB |
| Silero VAD | ~100 MB |
| faster-whisper tiny INT8 | ~75 MB |
| Qwen2.5-0.5B Q4_K_M | ~700 MB |
| Piper TTS (modelo medium) | ~150 MB |
| Buffer audio + app Python | ~100 MB |
| KV cache LLM (contexto activo) | ~500 MB |
| **Total estimado** | **~2.2 GB** |

Hay suficiente headroom (~5.8 GB libres). Para contexto de LLM más grande, limitar a 512 tokens de contexto.

---

### 5. Definición de Módulos (Interfaces Requeridas)

El agente DEBE implementar clases base abstractas (ABC) antes de escribir implementaciones concretas.

#### 5.1. Módulo de Audio (AudioInput)
```python
class AudioInput(ABC):
    @abstractmethod
    def start_stream(self) -> None: ...
    @abstractmethod
    def stop_stream(self) -> None: ...
    @abstractmethod
    def read_chunk(self) -> np.ndarray: ...
```

#### 5.2. Módulo de Wake Word (WakeWordDetector)
```python
class WakeWordDetector(ABC):
    @abstractmethod
    def process(self, audio_chunk: np.ndarray) -> bool: ...
    @abstractmethod
    def reset(self) -> None: ...
```
Implementación concreta: `PorcupineWakeWord(model_path="oye_robot.ppn", access_key=..., language="es")`.

#### 5.3. Módulo VAD (VoiceActivityDetector)
```python
class VoiceActivityDetector(ABC):
    @abstractmethod
    def is_speech(self, audio_chunk: np.ndarray) -> bool: ...
    @abstractmethod
    def reset(self) -> None: ...
```
Implementación concreta: `SileroVAD()`

#### 5.4. Módulo STT (SpeechToText)
```python
class SpeechToText(ABC):
    @abstractmethod
    def transcribe(self, audio: np.ndarray) -> str: ...
```
Implementaciones concretas: `GroqSTT(api_key, model="whisper-large-v3-turbo")`, `FasterWhisperSTT(model_size="tiny", compute_type="int8")`.

#### 5.5. Módulo Clasificador (IntentClassifier)
```python
class IntentClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> tuple[Intent, dict]: ...
```
Donde `Intent` es un Enum: `HABLAR, NAVEGAR_GIORNALE, NAVEGAR_BIOMEDICA, COMANDO_SIT, COMANDO_DANCE`.

Implementaciones concretas: `RegexIntentClassifier()` (Fase 2+), opcionalmente `ZeroShotIntentClassifier()` (Fase 4).

**Reglas Regex sugeridas para cada intent:**
- `NAVEGAR_GIORNALE`: r"(ir|voy|dirigir|navegar|llévame|muestra).*(giornale|periodico|noticias|diario)"
- `NAVEGAR_BIOMEDICA`: r"(ir|voy|dirigir|navegar|llévame|muestra).*(biomedica|medicina|lab|laboratorio)"
- `COMANDO_SIT`: r"(siéntate|sentar|sienta|sientate|sientese)"
- `COMANDO_DANCE`: r"(baila|bailar|danza|dance|muevete)"
- Si no matchea ninguna, por defecto: `HABLAR`

#### 5.6. Módulo LLM (TextGenerator)
```python
class TextGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None) -> Generator[str, None, None]: ...
```
Implementaciones concretas: `GroqLLM(api_key, model="llama-3.1-8b-instant")`, `LocalLLM(model_path="qwen2.5-0.5b-q4_k_m.gguf")`.

Debe generar texto fragmentado por oraciones (generator de strings) para permitir streaming en cascada.

#### 5.7. Módulo TTS (TextToSpeech)
```python
class TextToSpeech(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> np.ndarray: ...
    @abstractmethod
    def is_available(self) -> bool: ...
```
Implementaciones concretas: `DeepgramTTS(api_key, model="aura-2-thalia-en")`, `PiperTTS(model_path="es_ES-davefx-medium.onnx")`.

#### 5.8. Módulo Circuit Breaker (Resiliencia)
```python
class CircuitBreaker:
    state: Literal["ONLINE", "OFFLINE"]
    def check_connectivity(self) -> Literal["ONLINE", "OFFLINE"]: ...
    def get_stt(self) -> SpeechToText: ...  # devuelve impl online u offline según estado
    def get_llm(self) -> TextGenerator: ...
    def get_tts(self) -> TextToSpeech: ...
```

---

### 6. Guardarraíles y Contexto (Solo para intención HABLAR)

No se usa fine-tuning. Se usa Context Injection vía System Prompt.

**System Prompt para LLM (Cloud y Local):**
```text
Eres un asistente de navegación universitario amigable y conciso.
Hablas exclusivamente en español.
Contexto universitario: [INYECTAR TEXTO DEL USUARIO AQUÍ]
Reglas:
- Limita tu respuesta a MÁXIMO 1 oración (40 tokens como máximo).
- No uses saludos, presentaciones ni despedidas.
- Si te preguntan algo fuera del contexto universitario, responde "Eso no está en mi base de conocimiento universitaria".
- Responde SOLO preguntas sobre: horarios, ubicaciones de edificios, direcciones, eventos universitarios.
```

**Reglas adicionales:**
- `max_tokens=40` en todos los llamados LLM para intención `HABLAR`.
- Si el texto transcrito contiene groserías o lenguaje ofensivo, responder con comando predeterminado de cortesía.

---

### 7. Módulo de Resiliencia (Circuit Breaker)

- Timeout estricto: **800ms** en llamadas a APIs de Groq y Deepgram.
- Mecanismo: `concurrent.futures.ThreadPoolExecutor` con `future.result(timeout=0.8)`.
- Si la API falla o excede timeout, el estado cambia a `OFFLINE`.
- En `OFFLINE`, todas las interfaces conmutan automáticamente a implementaciones locales.
- Una vez en `OFFLINE`, reintentar cada 30 segundos con un ping a Groq (GET /models).
- Si el ping responde 2 veces consecutivas, volver a `ONLINE`.
- Publicar evento `STATE_CHANGED` ante cada transición de estado.

---

### 8. Módulo de Streaming en Cascada (Crucial para Latencia)

1. El LLM genera texto token por token (streaming).
2. El Orquestador acumula tokens en un buffer de fragmento.
3. Regex detecta signos de puntuación: `.` `,` `?` `!` `;`
4. Al detectar un signo, el fragmento acumulado se envía **inmediatamente** al Worker TTS.
5. El Worker TTS sintetiza el fragmento mientras el LLM continúa generando.
6. El audio sintetizado se reproduce sin esperar al texto completo.
7. Al finalizar el LLM, se envía el fragmento restante (si existe) al TTS.
8. **Consideración:** Deepgram TTS tiene límite de 2000 caracteres por request. Piper TTS no tiene límite práctico.

---

### 9. Fases de Implementación (Instrucciones para el Agente)

> **Para cada fase, leer la sección de input completo antes de comenzar. Al llegar a un paso que requiera datos del usuario, el agente DEBE detenerse y preguntar.**

#### Fase 0: Inicialización del Entorno
```bash
# Instalar uv si no está instalado
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crear proyecto
uv init proyectoProspectiva --python 3.10
cd proyectoProspectiva

# Crear estructura de directorios
mkdir -p src/procesos src/modulos src/interfaces tests modelos

# Activar entorno virtual
source .venv/bin/activate
```
El archivo `pyproject.toml` se usará para gestionar dependencias progresivamente.

#### Fase 1: Esqueleto y Bus de Eventos (Mocking)
**Objetivo:** Arquitectura base sin modelos reales.

**Tareas:**
1. Implementar `EventBus` usando `multiprocessing.Queue` y `multiprocessing.Pipe`.
   - `EventBus` debe ser thread-safe y process-safe.
   - Métodos: `publish(event_type, payload)`, `subscribe(event_type, callback)`, `unsubscribe(...)`.
   - Los callbacks se ejecutan en el proceso que se suscribe (no en el que publica).
2. Definir ABCs (Interfaces Abstractas) en `src/interfaces/`:
   - `stt.py`: `SpeechToText(ABC)`
   - `classifier.py`: `IntentClassifier(ABC)`
   - `llm.py`: `TextGenerator(ABC)`
   - `tts.py`: `TextToSpeech(ABC)`
   - `audio.py`: `AudioInput(ABC)`
   - `wake_word.py`: `WakeWordDetector(ABC)`
   - `vad.py`: `VoiceActivityDetector(ABC)`
3. Crear implementaciones Mock en `src/modulos/mocks/`:
   - Cada Mock imprime el payload recibido y hace `time.sleep(random.uniform(0.1, 0.5))`.
   - `MockSTT` devuelve texto fijo: "llévame a biomédica".
   - `MockClassifier` devuelve el intent basado en Regex sobre el texto fijo.
   - `MockLLM` devuelve fragmentos de texto oración por oración.
   - `MockTTS` guarda un archivo de silencio WAV.
4. Implementar `Orquestador` en `src/procesos/orquestador.py`:
   - Inicializa EventBus.
   - Lanza procesos hijo (Audio, Workers).
   - Maneja la máquina de estados simple (ONLINE/OFFLINE, modo mock).
5. Implementar `ProcesoAudio` en `src/procesos/audio.py`:
   - Lee chunks fijos de un archivo WAV pre-grabado (simula micrófono).
   - Publica eventos `WAKE_WORD_DETECTED` cada N chunks.
   - Publica `SPEECH_COMPLETED` con payload del chunk acumulado.
6. Implementar `ProcesoWorker` en `src/procesos/worker.py`:
   - Se suscribe a eventos.
   - Encadena STT → Classifier → LLM → TTS.
   - Publica cada resultado en el EventBus.
7. Validar: main.py lanza todos los procesos, el flujo completo corre con mocks.
8. Verificar con: `python src/main.py` — debe mostrar logs secuenciales del flujo.

**Dependencias a instalar:**
```bash
uv pip install numpy sounddevice
```

#### Fase 2: PoC en la Nube (Online Only)
**Objetivo:** Conectar micrófono real + APIs cloud.

**Requisitos previos del usuario:**
- `GROQ_API_KEY` (obtener en console.groq.com)
- `DEEPGRAM_API_KEY` (obtener en developers.deepgram.com)
- AccessKey de Picovoice Console (console.picovoice.ai) + descargar modelo `oye_robot.ppn` para Raspberry Pi.
- Texto universitario para System Prompt.

**Tareas:**
1. Instalar dependencias cloud:
   ```bash
   uv pip install groq>=1.3.0 deepgram-sdk pvporcupine>=4.0.2
   ```
2. Configurar variables de entorno (`.env`):
   ```
   GROQ_API_KEY=gsk_...
   DEEPGRAM_API_KEY=...
   PICOVOICE_ACCESS_KEY=...
   ```
3. Implementar `GroqSTT(src/modulos/stt/groq_stt.py)`:
   - Usar `client.audio.transcriptions.create(model="whisper-large-v3-turbo", file=...)`.
   - Timeout 800s vía `httpx` timeout.
   - Soporta archivos: FLAC, MP3, M4A, WAV, WEBM.
   - Debe convertir el audio numpy array a WAV bytes en memoria.
4. Implementar `GroqLLM(src/modulos/llm/groq_llm.py)`:
   - Usar `client.chat.completions.create(model="llama-3.1-8b-instant", messages=..., stream=True, max_tokens=40)`.
   - Devolver generator que emite fragmentos de texto.
   - System prompt con el texto universitario del usuario.
5. Implementar `DeepgramTTS(src/modulos/tts/deepgram_tts.py)`:
   - Usar `client.speak.v1.audio.generate(text=..., model="aura-2-thalia-en")`.
   - Devolver numpy array desde los bytes de audio resultantes.
6. Implementar grabación de audio básica con `sounddevice`:
   - `sounddevice.InputStream(callback=...)` con frecuencia 16000Hz, mono, dtype int16.
   - Grabar en bucle hasta que se presione Ctrl+C o haya silencio.
   - (Sin VAD ni wake word aún — solo grabar fragmento al presionar Enter.)
7. Implementar `RegexIntentClassifier`:
   - Según las reglas en sección 5.5.
   - Debe ejecutarse < 10ms (en CPU moderna es trivial).
8. Integrar todo: el orquestador ahora usa implementaciones reales cloud.
9. Verificar latencia E2E: desde que se presiona Enter hasta que se escucha respuesta.
   - Objetivo: < 2 segundos para modo ONLINE.
10. Implementar reproducción de audio con `sounddevice.OutputStream`.

#### Fase 3: Optimización de Entrada (VAD y Wake Word)
**Objetivo:** Activar por voz y eliminar silencio.

**Tareas:**
1. Instalar dependencias:
   ```bash
   uv pip install silero-vad onnxruntime
   ```
2. Configurar Porcupine:
   - Crear instancia: `pvporcupine.create(access_key=..., keyword_paths=["oye_robot.ppn"])`.
   - El modelo `oye_robot.ppn` se descarga de Picovoice Console (seleccionar plataforma Raspberry Pi).
   - Configurar sensibilidad (empezar con 0.5, ajustar si hay falsos positivos/negativos).
   - Nota: Porcupine requiere audio 16-bit, 16kHz, mono. El frame_length varía según modelo.
3. Integrar Porcupine en `ProcesoAudio`:
   - Bucle: leer chunk → `porcupine.process(chunk)` → si `result >= 0` publicar `WAKE_WORD_DETECTED`.
4. Integrar Silero VAD:
   - Después de wake word, alimentar chunks al VAD.
   - `vad.is_speech(chunk)` para cada chunk.
   - Cuando se detecte silencio por >= 500ms continuos (o timeout de 10s), publicar `SPEECH_COMPLETED`.
5. Configurar adecuadamente:
   - Frecuencia de muestreo: 16000 Hz (requerido por Porcupine y Silero).
   - Tamaño de chunk: 512 o 1024 samples (30-60ms).
   - Porcupine tiene su propio frame_length (usar `porcupine.frame_length`).
6. Prueba: decir "Oye Robot" → esperar pitido → dar comando → escuchar respuesta.
   - Verificar que no hay falsos positivos.
   - Verificar que el VAD corta correctamente.

#### Fase 4: Preparación para el Borde (Offline Fallback + Circuit Breaker)
**Objetivo:** Modelos locales + conmutación automática.

**Tareas:**
1. Instalar dependencias offline:
   ```bash
   uv pip install faster-whisper llama-cpp-python piper-tts huggingface-hub
   ```
2. Descargar modelos locales (TODO: preguntar al usuario rutas o descargar automáticamente).
   - STT: Descargar automático con `faster_whisper.WhisperModel(model_size_or_path="tiny", download_root="modelos/")`.
   - LLM: Descargar desde HuggingFace: `huggingface-cli download lmstudio-community/Qwen2.5-0.5B-Instruct-GGUF qwen2.5-0.5b-instruct-q4_k_m.gguf --local-dir modelos/`.
   - TTS: Descargar voz española: voz `es_ES-davefx-medium` desde HuggingFace (model.onnx + model.onnx.json).
3. Implementar `FasterWhisperSTT`:
   - `model = WhisperModel("tiny", device="cpu", compute_type="int8")`.
   - `segments, info = model.transcribe(audio, language="es", beam_size=1, vad_filter=True)`.
   - El audio debe ser float32 normalizado a [-1, 1], sample rate 16000.
4. Implementar `LocalLLM`:
   - `llm = llama_cpp.Llama(model_path="modelos/qwen2.5-0.5b-instruct-q4_k_m.gguf", n_ctx=512, n_threads=4, verbose=False)`.
   - `generator = llm.create_completion(prompt, max_tokens=40, stream=True, stop=["</s>", "\n", "."])`.
   - Sistema de chat: usar `llm.create_chat_completion(stream=True)` con mensajes estructurados.
   - Template de prompt para Qwen2.5: `<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_msg}<|im_end|>\n<|im_start|>assistant\n`.
5. Implementar `PiperTTS`:
   - Opción A (Python API): `from piper import PiperVoice; voice = PiperVoice.load(model_path)`.
   - Opción B (subprocess, más simple): `echo "{text}" | piper --model {model_path} --output-raw | aplay`.
   - Devolver audio como numpy array para reproducción con sounddevice.
   - Sample rate del modelo: 22050 Hz para es_ES-davefx-medium.
6. Implementar `CircuitBreaker` completo:
   - En el Orquestador, antes de cada operación cloud:
     1. Verificar timeout de 800ms.
     2. Si falla o excede, publicar `STATE_CHANGED("OFFLINE", razón)`.
     3. Reinicializar workers con implementaciones locales.
   - En estado OFFLINE:
     1. Cada 30 segundos, intentar GET a Groq API `/models`.
     2. Si responde OK 2 veces seguidas, publicar `STATE_CHANGED("ONLINE", "recovered")`.
     3. Reinicializar workers con implementaciones cloud.
7. Migrar el Clasificador: Opcionalmente reemplazar Regex con modelo Zero-Shot:
   - Evaluar si `cross-encoder/nli-distilroberta-base` cumple <10ms en RP5.
   - Si no, mantener Regex (es perfectamente viable para 5 intents).
8. Configurar streaming en cascada offline:
   - El LLM local genera tokens en un generator.
   - Regex por cada token acumulado buscando `. , ? ! ;`.
   - Fragmento completo → TTS (Piper) → reproducción inmediata.
   - El tiempo entre fragmentos debe ser < 200ms para sensación de fluidez.
9. Prueba completa:
   - Desconectar WiFi → verificar que el sistema conmuta a OFFLINE.
   - Decir "Oye Robot" + comando → verificar que funciona sin internet.
   - Reconectar WiFi → verificar que vuelve a ONLINE automáticamente.
   - Medir latencia E2E en modo OFFLINE (objetivo: < 5 segundos).
   - Verificar que comandos de navegación nunca se detienen incluso durante transición.

---

### 10. Entradas Requeridas del Usuario

> El agente DEBE detenerse y solicitar estos datos al llegar a la fase correspondiente.

#### Fase 2:
1. **GROQ_API_KEY** — obtener en https://console.groq.com
2. **DEEPGRAM_API_KEY** — obtener en https://developers.deepgram.com
3. **PICOVOICE_ACCESS_KEY** — obtener gratis en https://console.picovoice.ai (registro gratuito).
   - Además, generar el modelo `oye_robot.ppn` para Raspberry Pi desde el console.
4. **Texto universitario** — información de horarios, ubicaciones, nombres de edificios, eventos, etc. para inyectar en System Prompt.

#### Fase 4:
1. **Confirmación de descarga automática** de modelos:
   - faster-whisper tiny (~75MB)
   - Qwen2.5-0.5B-Instruct Q4_K_M (~400MB) — alternativa: Phi-3-mini-3.8B Q4_K_M (~2.3GB) si se desea más capacidad.
   - Piper es_ES-davefx-medium (~65MB)

#### Opcionales (cualquier fase):
1. Rutas a archivos `.wav` pregrabados para confirmación de comandos (ej. `voy_a_biomedica.wav`).
2. Voces alternativas de Piper TTS en español.

---

### 11. Estructura de Archivos del Proyecto

```
proyectoProspectiva/
├── pyproject.toml          # Dependencias (uv)
├── .env                    # API keys (no comitear)
├── modelos/                # Modelos locales descargados
│   ├── oye_robot.ppn       # Wake word Porcupine
│   ├── ggml-tiny.bin       # faster-whisper (descarga automática)
│   ├── qwen2.5-0.5b-q4_k_m.gguf  # LLM local
│   └── es_ES-davefx-medium.onnx   # Piper TTS
├── src/
│   ├── main.py             # Entry point
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── stt.py
│   │   ├── classifier.py
│   │   ├── llm.py
│   │   ├── tts.py
│   │   ├── audio.py
│   │   ├── wake_word.py
│   │   └── vad.py
│   ├── bus/
│   │   ├── __init__.py
│   │   └── event_bus.py
│   ├── modulos/
│   │   ├── mocks/
│   │   ├── stt/
│   │   │   ├── groq_stt.py
│   │   │   └── faster_whisper_stt.py
│   │   ├── classifier/
│   │   │   └── regex_classifier.py
│   │   ├── llm/
│   │   │   ├── groq_llm.py
│   │   │   └── local_llm.py
│   │   └── tts/
│   │       ├── deepgram_tts.py
│   │       └── piper_tts.py
│   ├── procesos/
│   │   ├── __init__.py
│   │   ├── orquestador.py
│   │   ├── audio.py
│   │   └── worker.py
│   └── utils/
│       ├── circuit_breaker.py
│       └── cascade_stream.py
└── tests/
    └── test_event_bus.py
```

---

### 12. Dependencias Completas (pyproject.toml)

```toml
[project]
name = "proyecto-prospectiva"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.24",
    "sounddevice>=0.5.5",
    "pvporcupine>=4.0.2",
    "silero-vad>=6.2",
    "onnxruntime>=1.15",
    "groq>=1.3.0",
    "deepgram-sdk>=3.0",
    "faster-whisper>=1.0",
    "llama-cpp-python>=0.3.20",
    "piper-tts>=1.4",
    "huggingface-hub>=0.20",
    "python-dotenv>=1.0",
]
```

---

### 13. Criterios de Aceptación por Fase

| Fase | Criterio |
|---|---|
| **Fase 1** | `python src/main.py` muestra logs de flujo completo con mocks. No hay crashes. |
| **Fase 2** | Decir comando → respuesta TTS en < 2 segundos con APIs cloud. |
| **Fase 3** | "Oye Robot" activa el sistema. Silencio corta grabación. Sin falsos positivos evidentes. |
| **Fase 4** | Desconectar WiFi → sistema sigue funcionando offline. Reconectar → vuelve a cloud. Latencia offline < 5s. |

---

