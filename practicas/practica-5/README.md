# Práctica 5 — Chatbot híbrido con Ollama y APIs externas

Extensión de la Práctica 4. El mismo chatbot cliente-servidor (frontend HTML/CSS/JS
+ backend FastAPI) deja de depender únicamente de Ollama local y ahora puede conversar
con un **modelo local** y con **modelos remotos** mediante **APIs externas**
(Google Gemini, Groq y OpenRouter), conservando los **perfiles de copiloto** y el
**`system_prompt`** editable.

El backend actúa como **capa intermedia**: recibe siempre el mismo formato de petición,
selecciona la función del proveedor correspondiente (`call_ollama`, `call_gemini`,
`call_openai_compatible`) y **normaliza las métricas** a un esquema común
(`wall_time_s`, `prompt_tokens`, `completion_tokens`, `total_tokens`,
`tokens_per_second`).

> Esta práctica es **sin estado** (stateless): cada petición es independiente, para que
> la comparación entre proveedores con el mismo prompt sea limpia. No usa SQLite.

## Requisitos cubiertos (Tema 5)

- Selección de **proveedor** (`ollama`, `gemini`, `groq`, `openrouter`).
- Selección de **modelo** (poblado dinámicamente según el proveedor vía `GET /providers`).
- Selección de **perfil de copiloto** y edición del **`system_prompt`**.
- Ajuste de `temperature`, `top_p` y `max_tokens`.
- Muestra respuesta, tokens de entrada/salida/totales y tiempo total.
- Manejo de errores de conexión, timeout y API key faltante.

## Estructura

```
practica-5/
├── backend/
│   ├── main.py          # API FastAPI: /, /health, /profiles, /providers, /chat
│   ├── requirements.txt # fastapi, uvicorn, requests, pydantic, python-dotenv, google-genai, openai
│   ├── .env             # Llaves privadas (NO se sube a git)
│   └── .env.example     # Plantilla sin llaves reales
└── frontend/
    ├── index.html       # Interfaz (proveedor + modelo + perfil + system prompt + parámetros)
    ├── styles.css       # Estilos
    └── app.js           # fetch a /chat, /profiles y /providers
```

## Proveedores y modelos

| Proveedor    | Modelos sugeridos                                                        | Requiere llave        |
|--------------|--------------------------------------------------------------------------|-----------------------|
| `ollama`     | `llama3.2:3b`, `qwen2.5:3b`, `qwen2.5:1.5b`, `llama3.2:1b`, `qwen2.5:0.5b`| No (local)            |
| `gemini`     | `gemini-2.5-flash`, `gemini-2.5-flash-lite`                              | `GEMINI_API_KEY`      |
| `groq`       | `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`                        | `GROQ_API_KEY`        |
| `openrouter` | `google/gemini-2.5-flash-lite`, `meta-llama/llama-3.1-8b-instruct:free`, `qwen/qwen-2.5-7b-instruct:free` | `OPENROUTER_API_KEY` |

> Nota: en este equipo se usa **Gemini a través de OpenRouter** con el modelo
> `google/gemini-2.5-flash-lite` (`OPENROUTER_API_KEY`). El proveedor `gemini` directo
> requiere una `GEMINI_API_KEY` propia; si no se define, devuelve un error controlado.

## Perfiles de copiloto

| Perfil          | Enfoque                                                        |
|-----------------|---------------------------------------------------------------|
| `generico`      | Asistente académico general.                                  |
| `docente`       | Diseño de clases, actividades, rúbricas y objetivos.          |
| `robotica`      | Sensores, actuadores, control; pide datos eléctricos faltantes.|
| `programacion`  | Python paso a paso; interpreta errores y da correcciones.     |
| `investigacion` | Preguntas de investigación; separa hechos/inferencias, no inventa citas.|

## Variables de entorno y seguridad

En `backend/` crea un archivo `.env` (ya incluido en `.gitignore`):

```
GEMINI_API_KEY=pega_aqui_tu_llave_de_gemini
GROQ_API_KEY=pega_aqui_tu_llave_de_groq
OPENROUTER_API_KEY=pega_aqui_tu_llave_de_openrouter
```

> El archivo `.env` no debe subirse a GitHub. Si una API key se publica por accidente,
> debe revocarse inmediatamente desde el panel del proveedor.

## Requisitos previos

- [Ollama](https://ollama.com) instalado y en ejecución (para el proveedor local).
- Python 3.10+.
- Llaves de API para los proveedores remotos que se vayan a usar.

## 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .\.venv\Scripts\Activate.ps1   # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env             # y completar las llaves
uvicorn main:app --reload --port 8000
```

- Documentación automática: http://localhost:8000/docs
- Perfiles: http://localhost:8000/profiles
- Proveedores y modelos: http://localhost:8000/providers

Probar el endpoint `/chat` con un proveedor remoto (Groq):

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explica qué es la odometría diferencial en un robot móvil de dos ruedas.",
    "provider": "groq",
    "model": "llama-3.3-70b-versatile",
    "copilot_profile": "robotica",
    "system_prompt": "",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 300
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

| Parámetro         | Rango            | Propósito                                   |
|-------------------|------------------|---------------------------------------------|
| `provider`        | 4 proveedores    | Elegir el motor (local o remoto)            |
| `model`           | según proveedor  | Elegir el modelo concreto                   |
| `copilot_profile` | 5 perfiles       | Elegir la identidad/rol del copiloto        |
| `system_prompt`   | texto editable   | Instrucción del sistema                     |
| `temperature`     | 0.0 – 1.2        | Controlar aleatoriedad                      |
| `top_p`           | 0.1 – 1.0        | Diversidad probabilística                   |
| `max_tokens`      | 20 – 1000        | Longitud máxima de salida                   |
| `num_ctx`         | 2048/4096/8192   | Ventana de contexto (solo Ollama)           |
| `repeat_penalty`  | 1.0 – 2.0        | Reducir repeticiones (solo Ollama)          |

## Métricas mostradas por respuesta

`wall_time_s` (tiempo del backend), `provider_duration_s`, `prompt_tokens` (entrada),
`completion_tokens` (salida), `total_tokens` y `tokens_per_second`. Además se muestra el
**proveedor**, el **modelo** y el **perfil usado**. En APIs externas las métricas dependen
de lo que reporte cada proveedor; el backend las convierte a este formato común.

## Endpoints

| Método | Endpoint     | Uso                                             |
|--------|--------------|-------------------------------------------------|
| `GET`  | `/`          | Información general de la API                   |
| `GET`  | `/health`    | Estado del servicio                             |
| `GET`  | `/profiles`  | Listar perfiles y sus system prompts            |
| `GET`  | `/providers` | Listar proveedores y modelos disponibles        |
| `POST` | `/chat`      | Enviar mensaje al proveedor/modelo seleccionado |
