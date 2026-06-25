# Quickstart

## 1. Backend

```bash
cd backend
source .venv/bin/activate          # o crea uno: python -m venv .venv
pip install -r requirements.txt
cp .env.example .env               # edita y agrega al menos una API key
uvicorn main:app --reload          # http://localhost:8000
```

## 2. Frontend

Abre `frontend/index.html` en el navegador, o sírvelo:

```bash
cd frontend
python -m http.server 3000         # http://localhost:3000
```

## Notas

- El frontend hace fetch a `http://localhost:8000` (`frontend/app.js:1`).
- Sin API keys el backend arranca, pero los providers cloud no responden.
- Ollama local: `ollama serve` + `ollama pull llama3.1`.
- Más detalles en `mdDocs/IMPLEMENTATION_SUMMARY.md`.