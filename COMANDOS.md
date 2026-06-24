# Sistema de Comandos - Documentación

## Cómo agregar nuevos comandos (en 3 pasos)

### Paso 1: Editar `config/commands.yaml`

Agregar una nueva entrada al final del archivo:

```yaml
commands:
  # ... comandos existentes ...

  - name: "COMANDO_SALUDAR"
    category: "robot"
    patterns:
      - "saluda"
      - "hola"
      - "buenos días"
    response: "¡Buenos días!"
    action: "wave"
    params: {}
```

### Paso 2: Reiniciar el asistente

```bash
# Detener (Ctrl+C) y volver a iniciar
uv run python src/prospectiva/main.py
```

### Paso 3: Probar

Di: "Oye Robot saluda" → El robot debería saludar.

## Estructura del YAML

```yaml
commands:
  - name: "NOMBRE_DEL_INTENT"      # Nombre único (ej: NAVEGAR_BIBLIOTECA)
    category: "navigation|robot"   # Categoría para organización
    patterns:                      # Lista de palabras clave que activan el comando
      - "palabra1"
      - "palabra2"
    response: "Texto de respuesta" # Lo que dice el TTS
    action: "nombre_accion"        # Acción a ejecutar (ver abajo)
    params: {}                     # Parámetros para la acción
```

## Acciones disponibles

### Navegación
- `navigate` → Navega a un destino (params: `destination: "BIOMEDICA"`)
- `get_location` → Obtiene ubicación actual
- `list_destinations` → Lista destinos disponibles

### Robot
- `sit` → Sentarse
- `stand` → Pararse
- `dance` → Bailar
- `wave` → Saludar
- `walk` → Caminar
- `stop` → Detenerse

### Conversación
- `llm` → Pasa al LLM para respuesta conversacional

## Categorías de intents

| Prefijo | Categoría | Ejemplo |
|---------|-----------|---------|
| `NAVEGAR_*` | Navegación | NAVEGAR_BIOMEDICA |
| `COMANDO_*` | Robot | COMANDO_SIT, COMANDO_DANCE |
| `HABLAR` | Conversación | Preguntas generales |

## Ejemplo completo: Agregar "ir a la biblioteca"

### 1. Agregar al YAML:
```yaml
  - name: "NAVEGAR_BIBLIOTECA"
    category: "navigation"
    patterns:
      - "biblioteca"
      - "biblio"
      - "llévame a la biblioteca"
    response: "Voy a la Biblioteca Central."
    action: "navigate"
    params:
      destination: "BIBLIOTECA"
```

### 2. Agregar al mapa de destinos (si es nuevo):

Editar `src/prospectiva/procesos/actions/navigation_actions.py`:
```python
DESTINATIONS = {
    # ... existentes ...
    "BIBLIOTECA": {
        "name": "Biblioteca Central", 
        "coordinates": [19.0, -98.0], 
        "url": "https://www.buap.mx/biblioteca"
    },
}
```

### 3. Reiniciar y probar

```bash
uv run python src/prospectiva/main.py
```

Di: "Oye Robot llévame a la biblioteca"

## Respuestas estructuradas del LLM

Cuando el intent es `HABLAR` (conversación general), el LLM devuelve JSON:

```json
{
    "response": "La biblioteca abre de 8am a 10pm.",
    "action": "none",
    "params": {},
    "confidence": 0.95
}
```

Si el LLM detecta que necesita ejecutar una acción:
```json
{
    "response": "Voy a la biblioteca.",
    "action": "navigate",
    "params": {"destination": "BIBLIOTECA"},
    "confidence": 0.98
}
```

## Arquitectura del sistema de acciones

```
Usuario habla
    ↓
Vosk (wake word) → Silero VAD → AudioProcess
    ↓
SPEECH_COMPLETED
    ↓
Groq STT (transcripción)
    ↓
ConfigurableClassifier (regex desde YAML)
    ↓
Intent: NAVEGAR_* / COMANDO_* / HABLAR
    ↓
┌─────────────────────────────────────────┐
│ NAVEGAR/COMANDO → ActionExecutor        │
│   → RobotActions.sit()                  │
│   → NavigationActions.navigate()        │
│   → TTS: confirmación                 │
├─────────────────────────────────────────┤
│ HABLAR → Groq LLM (JSON estructurado)  │
│   → Parse JSON                          │
│   → Ejecutar action si existe           │
│   → TTS: respuesta                      │
└─────────────────────────────────────────┘
    ↓
AUDIO_SYNTHESIZED → AudioPlayback → Speaker
```

## Para agregar acciones complejas (código)

Si necesitas una acción que no existe en `RobotActions` o `NavigationActions`:

1. Crear archivo en `src/prospectiva/procesos/actions/`:
```python
# custom_actions.py
class CustomActions:
    @staticmethod
    def my_custom_action(params):
        print("Ejecutando acción personalizada")
        return {"status": "ok", "data": "resultado"}
```

2. Registrar en `__init__.py`:
```python
from .custom_actions import CustomActions
executor.register("MI_ACCION", CustomActions.my_custom_action)
```

3. Agregar al YAML:
```yaml
  - name: "MI_ACCION"
    category: "custom"
    patterns:
      - "mi comando"
    response: "Hecho."
    action: "my_custom_action"
    params: {}
```

## Troubleshooting

### "No reconoce mi nuevo comando"
- Verificar que el YAML tiene sintaxis correcta (espacios, no tabs)
- Verificar que el patrón está en minúsculas
- Verificar que reiniciaste el asistente

### "La acción no se ejecuta"
- Verificar que el `action` en YAML coincide con el nombre registrado en el ActionExecutor
- Ver logs del Orquestador para ver el error

### "Quiero que el LLM maneje un comando nuevo"
- Dejar `patterns: []` en el YAML
- El LLM detectará el intent y devolverá el JSON con la acción
