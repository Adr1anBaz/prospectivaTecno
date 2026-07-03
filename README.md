# Prospectiva Tecnológica — IA Generativa y LLMs

Repositorio de prácticas y proyecto final del curso **IA Generativa y Prospectiva Tecnológica** (Verano 2026). Recorre, de forma incremental, el uso de modelos de lenguaje grande (LLM): desde la exploración de modelos locales hasta un chatbot híbrido que integra proveedores locales y remotos, y una arquitectura LLM que controla salidas vía MQTT.

- **Equipo:** Adrián Bazaldua, Fernando Pérez, Sebastián Enguilo
- **Sitio (GitHub Pages):** https://adr1anbaz.github.io/prospectivaTecno/
- **Repositorio:** https://github.com/Adr1anBaz/prospectivaTecno

## Prácticas

| # | Práctica | Descripción | Stack | Reporte |
|---|----------|-------------|-------|---------|
| 1 | [Panorama de IA Generativa y LLM](practicas/practica-1) | Exploración y comparativa de 6+ modelos locales | Ollama, Hugging Face | [Ver](https://adr1anbaz.github.io/prospectivaTecno/practica-1) |
| 2 | [Selección de plataforma y benchmark](practicas/practica-2) | Matriz de decisión + benchmark (100 ciclos/modelo) | Ollama | [Ver](https://adr1anbaz.github.io/prospectivaTecno/practica-2) |
| 3 | [Chatbot LLM local con contexto](practicas/practica-3) | Chatbot con contexto conversacional persistente | FastAPI, Ollama, SQLite | [Ver](https://adr1anbaz.github.io/prospectivaTecno/practica-3) |
| 4 | [Copilotos especializados](practicas/practica-4) | Perfiles de `system_prompt` y evaluación de prompting | FastAPI, Ollama, SQLite | [Ver](https://adr1anbaz.github.io/prospectivaTecno/practica-4) |
| 5 | [Chatbot híbrido con APIs externas](practicas/practica-5) | Capa multiproveedor: Ollama, Gemini, Groq, OpenRouter | FastAPI, google-genai, openai | [Ver](https://adr1anbaz.github.io/prospectivaTecno/practica-5) |
| 6 | [Arquitectura LLM + MQTT](practicas/practica-6) | Clasificación de intención (on/off/none) y publicación MQTT | FastAPI, Ollama, paho-mqtt | [Ver](https://adr1anbaz.github.io/prospectivaTecno/practica-6) |

Cada carpeta en `practicas/` contiene su propio `README.md` con instrucciones detalladas de ejecución.

## Estructura del repositorio

```
.
├── practicas/            # Código de cada práctica (practica-1 … practica-6)
│   ├── practica-1/       # Exploración de LLMs (Ollama + Hugging Face)
│   ├── practica-2/       # Matriz de decisión + benchmark
│   ├── practica-3/       # Chatbot FastAPI + Ollama + SQLite (contexto)
│   ├── practica-4/       # Copilotos especializados (perfiles de system prompt)
│   ├── practica-5/       # Chatbot híbrido (Ollama + Gemini + Groq + OpenRouter)
│   └── practica-6/       # Arquitectura LLM + MQTT (clasificación de intención)
├── docs/                 # Sitio de documentación (Jekyll + just-the-docs, GitHub Pages)
│   ├── index.md          # Página de inicio con el índice de prácticas
│   ├── practica-*.md     # Reporte de cada práctica (una página por práctica)
│   └── assets/, imgs/    # Datos crudos de baterías, gráficas y capturas
├── proyecto-final/       # Proyecto final
│   └── slides/           # Pitch deck (Vite + React, "Blu — Slides")
└── .github/workflows/    # CI: despliegue de GitHub Pages
```

## Tecnologías

- **Inferencia local:** [Ollama](https://ollama.com) (`llama3.2:3b`, `qwen2.5`, etc.).
- **Proveedores remotos:** Google Gemini, Groq y OpenRouter (Práctica 5).
- **Backend:** Python, FastAPI, Pydantic, Uvicorn.
- **Persistencia:** SQLite (SQLAlchemy) para el contexto conversacional (Prácticas 3 y 4).
- **Frontend:** HTML, CSS y JavaScript (sin framework).
- **Mensajería:** MQTT (`paho-mqtt`) en la Práctica 6.
- **Documentación:** Jekyll + [just-the-docs](https://just-the-docs.github.io/just-the-docs/), desplegado con GitHub Pages.
- **Proyecto final:** Vite + React (presentación).

## Requisitos previos

- Python 3.10+ (algunas prácticas se validaron con 3.12).
- [Ollama](https://ollama.com) instalado y en ejecución para las prácticas locales.
- Para la Práctica 5: llaves de API de los proveedores remotos que se vayan a usar (`GROQ_API_KEY`, `OPENROUTER_API_KEY`, opcionalmente `GEMINI_API_KEY`), definidas en `practicas/practica-5/backend/.env`.

## Cómo ejecutar una práctica

El patrón general (Prácticas 3, 4 y 5) es:

```bash
cd practicas/practica-N/backend
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
pip install -r requirements.txt
uvicorn main:app --port 8000

# En otra terminal, servir el frontend
cd practicas/practica-N/frontend
python3 -m http.server 5500
```

Consulta el `README.md` de cada práctica para los detalles (endpoints, parámetros, variables de entorno y baterías de prueba).

## Documentación y despliegue

El sitio se publica automáticamente en GitHub Pages al hacer push a `main` cuando cambian archivos de `docs/`. Para probarlo localmente:

```bash
cd docs
bundle install
bundle exec jekyll serve   # http://localhost:4000/prospectivaTecno/
```

## Licencia

Contenido académico para uso educativo.
