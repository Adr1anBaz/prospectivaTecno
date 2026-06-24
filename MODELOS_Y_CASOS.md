# Modelos de Voz y Casos de Uso del Sistema

## 📊 Modelos de Vosk Disponibles (Español)

| Modelo | Tamaño | Precisión (WER) | Uso | Recomendación |
|--------|--------|-----------------|-----|---------------|
| **vosk-model-small-es-0.42** | ~42MB | 16.02% (cv) | Móvil, RPi | ⚡ Rápido pero impreciso |
| **vosk-model-es-0.42** | ~1.4GB | 7.50% (cv) | Servidor | 🎯 Mucho más preciso, pesado |

**WER = Word Error Rate** (menor = mejor)
- 16% = 16 de cada 100 palabras mal transcritas
- 7.5% = 7-8 de cada 100 palabras mal transcritas

### Para Raspberry Pi 5
- El modelo small (~42MB) carga rápido y usa ~300MB RAM
- El modelo big (~1.4GB) es más preciso pero usa ~4GB RAM al cargar
- **RPi 5 con 8GB RAM puede manejar el big model**, pero tarda ~10-15 segundos en cargar

### Alternativa: Modelo Intermedio (Inglés como referencia)
Para inglés existe `vosk-model-en-us-0.22-lgraph` (~128MB) que es un compromiso entre velocidad y precisión. **Para español no existe un modelo intermedio oficial**.

### Otras Alternativas al Wake Word
Si Vosk sigue siendo impreciso para tu acento/voz:

1. **OpenWakeWord** (ONNX, ~400KB)
   - Requiere entrenar un modelo con tu voz diciendo "oye robot"
   - Más preciso que Vosk para wake words específicos
   - 100% offline después del entrenamiento
   - Se puede entrenar en Colab (gratis, 90 minutos)

2. **Porcupine (Picovoice)** (~1MB)
   - El más preciso para wake words
   - Requiere API key gratis (1 minuto registrarse)
   - Soporta "oye robot" nativamente
   - 100% offline después de generar el .ppn

3. **Whisper Tiny** (~75MB)
   - Mucho más preciso que Vosk para transcripción
   - No está diseñado para wake word detection en tiempo real
   - Podría usarse con un buffer circular para detectar "oye robot"

## 🔄 Diferentes Casos de Uso del Sistema

### Caso 1: Comando de Navegación
```
Usuario: "Oye Robot llévame a biomédica"

┌─────────────────────────────────────────────────┐
│ 1. Vosk detecta "oye robot" en partial result  │
│ 2. AudioProcess entra en LISTENING              │
│ 3. VAD detecta habla → bufferiza audio          │
│ 4. Silencio detectado → SPEECH_COMPLETED        │
│ 5. Groq STT transcribe: "Llévame a Biomédica"   │
│ 6. ConfigurableClassifier → NAVEGAR_BIOMEDICA    │
│ 7. ActionExecutor.execute()                     │
│    → NavigationActions.navigate()               │
│    → Result: {"destination": "BIOMEDICA", ...}   │
│ 8. Deepgram TTS: "Voy al edificio de Biomédica"│
│ 9. AudioPlayback reproduce el audio             │
│ 10. Cooldown 3s → vuelve a escuchar wake word   │
└─────────────────────────────────────────────────┘

Console output:
============================================================
  🤖 ACCIÓN EJECUTADA
============================================================
  • Comando: 'Llévame a Biomédica'
  • Intent detectado: NAVEGAR_BIOMEDICA
  • Acción ejecutada: navigate
  • Status: completed
  • Respuesta TTS: 'Voy al edificio de Biomédica'
============================================================
```

### Caso 2: Comando del Robot
```
Usuario: "Oye Robot siéntate"

┌─────────────────────────────────────────────────┐
│ 1. Vosk detecta "oye robot"                      │
│ 2. AudioProcess LISTENING → VAD                 │
│ 3. SPEECH_COMPLETED: "siéntate"                   │
│ 4. Groq STT: "siéntate"                         │
│ 5. Classifier → COMANDO_SIT                      │
│ 6. ActionExecutor.execute()                     │
│    → RobotActions.sit()                         │
│    → Result: {"action": "sit", "status": "ok"}   │
│ 7. TTS: "Me siento"                             │
│ 8. AudioPlayback reproduce                       │
└─────────────────────────────────────────────────┘

Console output:
============================================================
  🤖 ACCIÓN EJECUTADA
============================================================
  • Comando: 'siéntate'
  • Intent detectado: COMANDO_SIT
  • Acción ejecutada: sit
  • Status: completed
  • Respuesta TTS: 'Me siento'
============================================================
```

### Caso 3: Conversación General (LLM)
```
Usuario: "Oye Robot ¿qué horario tiene la biblioteca?"

┌─────────────────────────────────────────────────┐
│ 1. Vosk detecta "oye robot"                      │
│ 2. AudioProcess LISTENING → VAD                 │
│ 3. SPEECH_COMPLETED: "¿qué horario...?"         │
│ 4. Groq STT: "¿qué horario tiene la biblioteca?"│
│ 5. Classifier → HABLAR (no match en patterns)   │
│ 6. LLM.generate() con prompt estructurado         │
│ 7. LLM devuelve JSON:                           │
│    {                                            │
│      "response": "La biblioteca abre de 8am a", │
│      "action": "none",                          │
│      "params": {},                              │
│      "confidence": 0.95                         │
│    }                                            │
│ 8. Parse JSON → TTS: "La biblioteca abre..."    │
│ 9. AudioPlayback reproduce                       │
└─────────────────────────────────────────────────┘

Console output:
============================================================
  🧠 RESPUESTA LLM (JSON ESTRUCTURADO)
============================================================
  • Pregunta: '¿qué horario tiene la biblioteca?'
  • Respuesta: 'La biblioteca abre de 8am a 10pm'
  • Action sugerida: none
  • Params: {}
  • Confidence: 0.95
============================================================
```

### Caso 4: Conversación + Acción (LLM detecta acción)
```
Usuario: "Oye Robot necesito ir a la biblioteca"

┌─────────────────────────────────────────────────┐
│ 1. Vosk detecta "oye robot"                      │
│ 2. AudioProcess LISTENING → VAD                 │
│ 3. SPEECH_COMPLETED: "necesito ir a la biblio"  │
│ 4. Groq STT: "necesito ir a la biblioteca"      │
│ 5. Classifier → HABLAR (no match exacto)         │
│ 6. LLM.generate()                                │
│ 7. LLM devuelve JSON:                           │
│    {                                            │
│      "response": "Voy a la biblioteca",         │
│      "action": "navigate",                      │
│      "params": {"destination": "BIBLIOTECA"},   │
│      "confidence": 0.98                         │
│    }                                            │
│ 8. Parse JSON → ActionExecutor.execute()        │
│    → NavigationActions.navigate()                │
│ 9. TTS: "Voy a la biblioteca"                   │
│ 10. AudioPlayback reproduce                      │
└─────────────────────────────────────────────────┘

Console output:
============================================================
  🧠 RESPUESTA LLM (JSON ESTRUCTURADO)
============================================================
  • Pregunta: 'necesito ir a la biblioteca'
  • Respuesta: 'Voy a la biblioteca'
  • Action sugerida: navigate
  • Params: {"destination": "BIBLIOTECA"}
  • Confidence: 0.98
============================================================
```

### Caso 5: Timeout (no hay comando)
```
Usuario: "Oye Robot" (y no dice nada más)

┌─────────────────────────────────────────────────┐
│ 1. Vosk detecta "oye robot"                      │
│ 2. AudioProcess LISTENING → VAD                 │
│ 3. Timeout después de 8 segundos sin habla      │
│ 4. AudioProcess vuelve a WAKE_WORD               │
│ 5. No hay SPEECH_COMPLETED                       │
│ 6. Orquestador no hace nada                      │
└─────────────────────────────────────────────────┘

Console output:
[AudioProcess] ⏱ Listening timeout (8s), no command detected
[AudioProcess] Back to wake word listening
```

### Caso 6: Cooldown (evita loop por feedback)
```
Usuario: "Oye Robot siéntate" (el speaker dice "Me siento")

┌─────────────────────────────────────────────────┐
│ 1. Vosk detecta "oye robot"                      │
│ 2. AudioProcess LISTENING → VAD                 │
│ 3. SPEECH_COMPLETED → procesa → TTS            │
│ 4. AudioPlayback reproduce "Me siento"            │
│ 5. AudioProcess entra en COOLDOWN (3s)          │
│ 6. Durante cooldown: NO escucha wake word       │
│ 7. Cooldown termina → vuelve a WAKE_WORD        │
│ 8. El audio del speaker no re-activa el sistema │
└─────────────────────────────────────────────────┘

Console output:
[AudioProcess] Cooldown ended, listening for wake word
```

## 🔧 Cambiar el Modelo de Vosk

### Opción 1: Modelo Grande (más preciso, ~1.4GB)
```bash
# Descargar el modelo grande
wget https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip
unzip vosk-model-es-0.42.zip

# Actualizar .env
VOSK_MODEL_PATH=./models/vosk/vosk-model-es-0.42
```

### Opción 2: Usar OpenWakeWord (más preciso para wake word)
```bash
# Requiere entrenamiento en Colab
# Ver: https://github.com/dscripka/openWakeWord
# Entrena con "oye robot" y descarga el .onnx
```

### Opción 3: Porcupine (Picovoice) - Más preciso
```bash
# Regístrate gratis en console.picovoice.ai
# Genera "oye robot" en español
# Descarga el .ppn
# Usa el código anterior de PorcupineWakeWord
```

## 📋 Troubleshooting

### "No detecta mi voz"
- Prueba el modelo grande de Vosk (~1.4GB)
- Ajusta el umbral del VAD: `SileroVAD(threshold=0.3)` (más sensible)
- Verifica que el micrófono funciona: `arecord -l`

### "Transcribe palabras incorrectas"
- El modelo small es impreciso por diseño (16% WER)
- Usa el modelo grande (7.5% WER) o Whisper
- Entrena un modelo personalizado con Vosk

### "El sistema se activa solo"
- El cooldown está funcionando (3s después de respuesta)
- Ajusta `cooldown_seconds` en VoskWakeWord
- Considera usar Porcupine (más preciso para wake words)

### "No escucha el comando"
- El grace period puede ser corto para tu ritmo de habla
- Ajusta `_grace_period_chunks` en AudioProcess
- Ajusta `_max_silence` para dar más tiempo antes de finalizar
