# Práctica 3 — Chatbot web con LLM local y contexto (Ollama + SQLite)

Chatbot cliente-servidor que conversa con un modelo LLM local mediante Ollama.
El frontend (HTML/CSS/JS) envía los mensajes a una API en Python (FastAPI), que
actúa como intermediaria hacia Ollama, mantiene el **contexto conversacional**
en una base de datos **SQLite**, mide métricas y devuelve un JSON estructurado.

Cumple los requerimientos mínimos de la práctica (backend FastAPI, `POST /chat`,
conexión a Ollama, frontend con parámetros configurables y métricas por respuesta)
y añade contexto persistente: cada conversación guarda su historial y el backend lo
reenvía a Ollama turno a turno.

## Estructura

```
practica-3/
├── backend/
│   ├── main.py          # API FastAPI: /, /health, /chat, /conversations
│   ├── database.py      # SQLite (tablas conversations y messages)
│   ├── chatbot.db       # Base de datos (se genera al ejecutar)
│   └── requirements.txt # fastapi, uvicorn, requests, pydantic, SQLAlchemy
└── frontend/
    ├── index.html       # Interfaz
    ├── styles.css       # Estilos
    └── app.js           # Comunicación con el backend (fetch) + conversation_id
```

## Cómo funciona el contexto

1. El primer mensaje se envía con `conversation_id: null`; el backend crea una
   conversación nueva en SQLite y devuelve su `conversation_id`.
2. El frontend guarda ese `conversation_id` y lo reenvía en cada mensaje siguiente.
3. En cada turno el backend recupera el historial de esa conversación, lo concatena
   con el `system` y el mensaje nuevo, y envía todo a Ollama (`/api/chat`).
4. Se guardan en SQLite tanto el mensaje del usuario como la respuesta del asistente.
5. El botón **Limpiar conversación** reinicia el `conversation_id` (empieza de cero).

## Requisitos previos

- [Ollama](https://ollama.com) instalado y en ejecución.
- Al menos un modelo local descargado. Modelos disponibles en este equipo:
  `llama3.2:3b`, `qwen2.5:3b`, `qwen2.5:1.5b`, `llama3.2:1b`, `qwen2.5:0.5b`.
- Python 3.10+.

```bash
# Verificar Ollama y modelos
ollama --version
ollama list

# (si falta el modelo por defecto)
ollama pull llama3.2:3b
```

## 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .\.venv\Scripts\Activate.ps1   # Windows PowerShell

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

- Documentación automática: http://localhost:8000/docs
- Salud: http://localhost:8000/health

Probar el endpoint `/chat`:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explica qué es un sensor ultrasónico en máximo 80 palabras.",
    "model": "llama3.2:3b",
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 120,
    "num_ctx": 4096,
    "repeat_penalty": 1.1
  }'
```

## 2. Frontend

En otra terminal:

```bash
cd frontend
python3 -m http.server 5500
```

Abrir http://localhost:5500 en el navegador.

## Parámetros configurables

| Parámetro        | Rango        | Propósito                       |
|------------------|--------------|---------------------------------|
| `model`          | instalados   | Elegir LLM local                |
| `temperature`    | 0.0 – 1.2    | Controlar aleatoriedad          |
| `top_p`          | 0.1 – 1.0    | Diversidad probabilística       |
| `num_predict`    | 20 – 1000    | Longitud máxima de salida       |
| `num_ctx`        | 2048/4096/8192 | Ventana de contexto           |
| `repeat_penalty` | 1.0 – 2.0    | Reducir repeticiones            |

## Métricas mostradas por respuesta

`wall_time_s` (backend), `total_duration_s`, `load_duration_s`,
`prompt_eval_count` (tokens entrada), `eval_count` (tokens salida),
`total_tokens`, `eval_duration_s` y `tokens_per_second`.

> Al continuar una conversación, verás cómo `prompt_eval_count` (tokens de entrada)
> crece turno a turno: esa es la evidencia de que el historial se está enviando a Ollama.

## Endpoints de conversaciones (contexto)

| Método   | Endpoint                    | Uso                          |
|----------|-----------------------------|------------------------------|
| `POST`   | `/chat`                     | Enviar mensaje (crea/usa conversación) |
| `GET`    | `/conversations`            | Listar conversaciones        |
| `GET`    | `/conversations/{id}`       | Ver historial de una conversación |
| `DELETE` | `/conversations/{id}`       | Borrar una conversación      |
