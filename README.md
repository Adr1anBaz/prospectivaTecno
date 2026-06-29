# Asistente de Voz Universitario — Blu

Asistente de navegación e información para campus universitario. Wake word offline, STT/LLM/TTS online, integración con servidor MCP y Route API.

> Rama activa de desarrollo: `main`

---

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) para manejo de dependencias
- API keys:
  - **Groq** (`GROQ_API_KEY`): https://console.groq.com
  - **Deepgram** (`DEEPGRAM_API_KEY`): https://developers.deepgram.com
- (Opcional) Cuenta de Google Cloud con **Cloud Speech-to-Text API** habilitada

---

## Instalación

```bash
# 1. Clonar la rama main
git clone -b main https://github.com/Adr1anBaz/prospectivaTecno.git
cd prospectivaTecno

# 2. Crear .env a partir del ejemplo
cp .env.example .env

# 3. Editar .env con tus API keys
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

---

## Modo de ejecución

### Modo audio (normal)

Usa el micrófono. Di `"ronaldo"` seguido del comando.

```bash
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
🗣️ Entrando a modo conversación...

🗣️  > gracias
🧠 RESPUESTA CONVERSACIONAL
  ...

🗣️  > /end
🔇 Modo conversación terminado.

🎤 [ronaldo] > /exit
👋 Saliendo...
```

---

## Configuración de STT

El motor de Speech-to-Text se elige con `STT_PROVIDER` en `.env`:

```bash
# Opciones: groq | deepgram | googlecloud
STT_PROVIDER=groq
```

### Google Cloud Speech-to-Text (recomendado para mejor precisión)

1. Ve a [Google Cloud Console → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Crea un service account con rol **Cloud Speech-to-Text API User**
3. Genera una clave JSON y guárdala en tu proyecto, por ejemplo:
   ```
   ./credentials/gcp-speech.json
   ```
4. En `.env`:
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS=./credentials/gcp-speech.json
   STT_PROVIDER=googlecloud
   ```

> **Importante:** Nunca subas la carpeta `credentials/` a git. Ya está en `.gitignore`.

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

## Configuración de TTS

```bash
# Opciones: deepgram | local
TTS_PROVIDER=deepgram
TTS_MODEL=aura-2-celeste-es
```

La voz por defecto es `aura-2-celeste-es`. Otras opciones en español:
- `aura-2-alejandra-es`
- `aura-2-sofia-es`
- `aura-2-marcos-es`
- `aura-2-octavio-es`

---

## Funcionalidades principales

- **Wake word**: `"ronaldo"` detectada offline con Vosk
- **STT**: Groq Whisper, Deepgram Nova-3 o Google Cloud Speech-to-Text
- **TTS**: Deepgram Aura-2 en español
- **Navegación**: comandos directos a edificios del campus
- **Robot**: comandos de movimiento (`siéntate`, `baila`, `camina`, etc.)
- **Conversación**: LLM con tool calling nativo sobre 15 herramientas MCP
- **Modo conversación**: tras una respuesta, el asistente sigue escuchando sin repetir wake word
- **Modo texto**: prueba todo sin micrófono

---

## Estructura del proyecto

```
src/prospectiva/
├── main.py                 # Punto de entrada y orquestación de procesos
├── bus/
│   └── event_bus.py        # Bus de eventos entre procesos
├── modulos/
│   ├── llm/                # Groq LLM
│   ├── stt/                # STT providers (Groq, Deepgram, Google Cloud)
│   ├── tts/                # TTS providers (Deepgram, Local mock)
│   ├── muta/               # Audio input, VAD, wake word
│   └── classifier/         # Clasificador de intents
├── procesos/
│   ├── audio.py            # Proceso de audio (micrófono)
│   ├── text_input.py       # Modo texto (stdin)
│   ├── orquestador.py      # Orquestador central
│   ├── playback.py         # Reproducción de audio
│   └── movement.py         # Ejecución de movimientos
└── utils/                  # MCP client, Route client, audio utils
```

---

## Notas

- El proyecto usa **multiprocessing**. En modo audio usa `spawn`; en modo texto usa `fork` para evitar problemas con stdin.
- El modo `--test` usa clientes MCP y Route mock para pruebas sin levantar servidores.
- La carpeta `credentials/` está ignorada en git para proteger las claves de Google Cloud.
