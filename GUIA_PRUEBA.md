# Guía de Prueba Paso a Paso - Asistente de Voz Universitario

## ✅ Prerrequisitos

1. **Archivo `.env` creado** con tus API keys:
```bash
cp .env.example .env
# Editar .env y agregar:
# GROQ_API_KEY=gsk_...
# DEEPGRAM_API_KEY=...
# VOSK_MODEL_PATH=./models/vosk/vosk-model-small-es-0.42
```

2. **Modelo Vosk descargado**:
```bash
uv run python scripts/download_vosk_model.py
```

## ▶️ Ejecutar el Asistente

```bash
uv run python src/prospectiva/main.py
```

## 👀 Lo que DEBERÍAS VER en la terminal

### 1. Inicio exitoso
```
============================================================
Asistente de Voz Universitario - ONLINE ONLY
============================================================
Started process: AudioProcess (PID=12345)
Started process: Orquestador (PID=12346)
Started process: AudioPlayback (PID=12347)
✅ Asistente iniciado. Dime 'Oye Robot' para activar.
Presiona Ctrl+C para detener.
```

### 2. Wake Word detectado
```
[AudioProcess] Wake word detected!
```

### 3. VAD detectando voz
```
[AudioProcess] Speech completed: 24000 samples
```

### 4. Orquestador procesando
```
[Orquestador] Transcribed: "llévame a biomédica"
[Orquestador] Intent: NAVEGAR_BIOMEDICA
[Orquestador] Navigating to: https://www.buap.mx/biomedica
[Orquestador] Synthesizing: "Abriendo biomédica"
[Orquestador] Audio synthesized: 24000 bytes
```

### 5. Audio reproduciendo
```
[AudioPlayback] Playing audio: 24000 bytes
```

## 🗣️ Qué DECIR para probar

### Prueba 1: Navegación
1. Di: **"Oye Robot"** (espera el tono de confirmación)
2. Di: **"llévame a biomédica"** o **"voy al giornale"**
3. Deberías escuchar: **"Abriendo biomédica"** o similar
4. Debería abrirse: el navegador con la URL correspondiente

### Prueba 2: Comandos
1. Di: **"Oye Robot"**
2. Di: **"siéntate"** o **"baila"**
3. Deberías escuchar una confirmación del comando

### Prueba 3: Conversación general
1. Di: **"Oye Robot"**
2. Di: **"¿qué horario tiene la biblioteca?"**
3. Deberías escuchar una respuesta corta del LLM

## 🔄 Flujo de eventos esperado

```
Tú: "Oye Robot"
  ↓
Vosk: WAKE_WORD_DETECTED
  ↓
SileroVAD: empieza a grabar
  ↓
Tú: "llévame a biomédica"
  ↓
SileroVAD: detecta silencio
  ↓
Event: SPEECH_COMPLETED (audio_bytes)
  ↓
GroqSTT: transcripción → "llévame a biomédica"
  ↓
RegexClassifier: Intent=NAVEGAR_BIOMEDICA
  ↓
GroqLLM: "Abriendo biomédica"
  ↓
DeepgramTTS: audio_bytes
  ↓
Event: AUDIO_SYNTHESIZED
  ↓
AudioPlayback: reproduce por el speaker
```

## 🛠️ Si algo falla

### Error: "No se pudo inicializar audio/wake_word"
- Verifica que el modelo Vosk existe: `ls models/vosk/vosk-model-small-es-0.42/`
- Si no existe: `uv run python scripts/download_vosk_model.py`

### Error: "GROQ_API_KEY not found"
- Verifica `.env`: `cat .env`
- Asegúrate de que las variables no tengan comentarios al final

### Error: "VoskWakeWord process failed"
- Puede ser un problema con el micrófono. Verifica: `arecord -l`
- Si no hay micrófono, el asistente no puede funcionar sin hardware

### Error: No detecta "Oye Robot"
- Habla claro y cerca del micrófono
- Prueba variantes: "oye robot", "oye robots", "hoy robot"
- Vosk usa gramática limitada, puede ser menos preciso que Porcupine

### Error: No hay audio de salida
- Verifica el speaker: `speaker-test -t sine -f 1000`
- Si no hay salida, verifica la configuración de ALSA/PulseAudio

## 🧪 Tests automatizados

```bash
# Test de arquitectura (sin hardware)
uv run python tests/test_e2e_mock.py

# Test de multiprocessing (verifica que los procesos funcionan)
uv run python tests/test_multiprocessing_spawn.py
```

## 📋 Checklist final

- [ ] `.env` tiene GROQ_API_KEY y DEEPGRAM_API_KEY
- [ ] Modelo Vosk descargado en `models/vosk/vosk-model-small-es-0.42`
- [ ] `uv run python tests/test_multiprocessing_spawn.py` pasa
- [ ] `uv run python src/prospectiva/main.py` inicia sin errores
- [ ] Micrófono detectado por el sistema
- [ ] Speaker/auriculares funcionan
- [ ] Dices "Oye Robot" y detecta wake word
- [ ] Das un comando y responde con audio

## 🎉 Éxito

Si todo funciona, tienes un asistente de voz universitario funcional con:
- **Wake word offline**: Vosk ("Oye Robot")
- **STT**: Groq Whisper (online)
- **LLM**: Groq Llama (online)
- **TTS**: Deepgram Aura (online)
- **VAD**: Silero (offline)
