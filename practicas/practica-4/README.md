# Práctica 4 — Copilotos especializados con Ollama (prompting + contexto)

Extensión de la Práctica 3. El mismo chatbot cliente-servidor (frontend HTML/CSS/JS
+ backend FastAPI + Ollama) se convierte en un **copiloto especializado** mediante
**perfiles de system prompt**. Ahora el usuario, además de escribir un mensaje y
ajustar parámetros, puede **seleccionar un perfil de copiloto** y **editar el
`system_prompt`** que define rol, reglas, límites y formato del modelo.

Se conserva el **contexto conversacional** en **SQLite** (heredado de la Práctica 3):
cada conversación guarda su historial y el backend lo reenvía a Ollama turno a turno,
colocando el `system_prompt` del perfil como `messages[0]`.

## Requerimientos cubiertos (Tema 4)

1. Selector de perfil de copiloto en el frontend.
2. Cinco perfiles predefinidos (≥ 3): genérico, docente, robótica, programación, investigación.
3. Campo editable para `system_prompt`.
4. Backend que usa el `system_prompt` en `messages[0]`.
5. Endpoint `GET /profiles`.
6. Visualización de respuesta, perfil usado y métricas de inferencia.
7. Comparación entre asistente genérico y copiloto especializado (nota guía en la UI).

## Estructura

```
practica-4/
├── backend/
│   ├── main.py          # API FastAPI: /, /health, /profiles, /chat, /conversations
│   ├── database.py      # SQLite (tablas conversations y messages)
│   ├── chatbot.db       # Base de datos (se genera al ejecutar)
│   └── requirements.txt # fastapi, uvicorn, requests, pydantic, SQLAlchemy
└── frontend/
    ├── index.html       # Interfaz (perfil + system prompt + parámetros)
    ├── styles.css       # Estilos
    └── app.js           # fetch a /chat y /profiles + conversation_id
```

## Perfiles de copiloto

| Perfil          | Enfoque                                                        |
|-----------------|---------------------------------------------------------------|
| `generico`      | Asistente académico general.                                  |
| `docente`       | Diseño de clases, actividades, rúbricas y objetivos.          |
| `robotica`      | Sensores, actuadores, control; pide datos eléctricos faltantes.|
| `programacion`  | Python paso a paso; interpreta errores y da correcciones.     |
| `investigacion` | Preguntas de investigación; separa hechos/inferencias, no inventa citas.|

- Al elegir un perfil (o pulsar **Cargar plantilla**), su `system_prompt` se carga
  en el textarea y puede editarse libremente antes de enviar.
- Si el `system_prompt` enviado está vacío, el backend usa el del perfil por defecto.

## Cómo funciona el contexto

1. El primer mensaje se envía con `conversation_id: null`; el backend crea una
   conversación nueva en SQLite y devuelve su `conversation_id`.
2. El frontend guarda ese `conversation_id` y lo reenvía en cada mensaje siguiente.
3. En cada turno el backend arma `messages`: el `system_prompt` del perfil, el
   historial de la conversación y el mensaje nuevo, y lo envía a Ollama (`/api/chat`).
4. Se guardan en SQLite el mensaje del usuario y la respuesta del asistente.
5. El botón **Limpiar conversación** reinicia el `conversation_id` (empieza de cero).

## Requisitos previos

- [Ollama](https://ollama.com) instalado y en ejecución.
- Al menos un modelo local descargado. Modelos disponibles en este equipo:
  `llama3.2:3b`, `qwen2.5:3b`, `qwen2.5:1.5b`, `llama3.2:1b`, `qwen2.5:0.5b`.
- Python 3.10+.

```bash
ollama --version
ollama list
ollama pull llama3.2:3b   # si falta el modelo por defecto
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
- Perfiles disponibles: http://localhost:8000/profiles

Probar el endpoint `/chat` con un perfil especializado:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cómo conecto un sensor ultrasónico HC-SR04?",
    "model": "llama3.2:3b",
    "copilot_profile": "robotica",
    "system_prompt": "",
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 180,
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

| Parámetro         | Rango            | Propósito                          |
|-------------------|------------------|------------------------------------|
| `model`           | instalados       | Elegir LLM local                   |
| `copilot_profile` | 5 perfiles       | Elegir la identidad/rol del copiloto |
| `system_prompt`   | texto editable   | Instrucción persistente del sistema |
| `temperature`     | 0.0 – 1.2        | Controlar aleatoriedad             |
| `top_p`           | 0.1 – 1.0        | Diversidad probabilística          |
| `num_predict`     | 20 – 1000        | Longitud máxima de salida          |
| `num_ctx`         | 2048/4096/8192   | Ventana de contexto                |
| `repeat_penalty`  | 1.0 – 2.0        | Reducir repeticiones               |

## Métricas mostradas por respuesta

`wall_time_s` (backend), `total_duration_s`, `load_duration_s`,
`prompt_eval_count` (tokens entrada), `eval_count` (tokens salida),
`total_tokens`, `eval_duration_s` y `tokens_per_second`. Además se muestra el
**perfil usado** y el **modelo** de la última respuesta.

## Endpoints

| Método   | Endpoint                    | Uso                                    |
|----------|-----------------------------|----------------------------------------|
| `GET`    | `/profiles`                 | Listar perfiles y sus system prompts   |
| `POST`   | `/chat`                     | Enviar mensaje (crea/usa conversación) |
| `GET`    | `/conversations`            | Listar conversaciones                  |
| `GET`    | `/conversations/{id}`       | Ver historial de una conversación      |
| `DELETE` | `/conversations/{id}`       | Borrar una conversación                |
