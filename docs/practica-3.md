---
layout: default
title: Práctica 3
nav_order: 4
description: "Chatbot LLM Local con Contexto usando SQLite"
---

# Práctica 3: Chatbot LLM Local con Contexto
{: .fs-9 }

Sistema de chatbot web con gestión de contexto conversacional usando Ollama, FastAPI y SQLite.
{: .fs-6 .fw-300 }

[Ver en GitHub](https://github.com/Adr1anBaz/prospectivaTecno/tree/main/practicas){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 }

---

## 📋 Información General

| Campo | Detalle |
|:------|:--------|
| **Alumnos** | Adrián Bazaldua, Fernando Pérez, Sebastián Enguilo |
| **Fecha** | Julio 2026 |
| **Práctica** | #3 - Chatbot con Contexto y Base de Datos |
| **Modelo** | `llama3.2:3b` (Q4_K_M, 2.0 GB) vía Ollama local |
| **Backend** | FastAPI en `127.0.0.1:8002` |
| **Frontend** | HTML/CSS/JS en `localhost:5500` |

---

## 🎯 Características

- Contexto conversacional persistente por conversación (SQLite)
- API REST: crear / listar / obtener / eliminar conversaciones
- Métricas por respuesta: wall time, tokens entrada/salida, velocidad
- Configuración de parámetros desde el frontend (`temperature`, `top_p`, `num_predict`, `num_ctx`, `repeat_penalty`)

---

## 📐 Arquitectura

```
Usuario → Frontend (HTML/JS, puerto 5500)
        → Backend FastAPI (puerto 8002)
            → recupera historial de SQLite
            → llama a Ollama (puerto 11434) con messages[]
            → guarda par user/assistant en SQLite
        ← JSON { reply, metrics }
```

El navegador **nunca** habla directo con Ollama: el backend valida, mide y estructura la respuesta.

---

## 🗂️ Estructura

```
practicas/
├── backend/
│   ├── main.py              # FastAPI: /chat, /conversations
│   ├── database.py          # SQLAlchemy (conversations, messages)
│   ├── chatbot.db           # SQLite (generado)
│   ├── requirements.txt
│   └── migrate_db.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── test_context_with_db.py  # demo manual de contexto
├── test_metrics_battery.py  # batería de métricas (este doc la usa)
└── docs/assets/practica-3/  # JSON crudos y resumen
```

---

## 🔌 API esencial

| Método | Endpoint | Uso |
|--------|----------|-----|
| `POST` | `/chat` | Enviar mensaje; recibe `conversation_id` |
| `GET`  | `/conversations` | Listar conversaciones |
| `GET`  | `/conversations/{id}` | Obtener historial |
| `DELETE` | `/conversations/{id}` | Borrar conversación |
| `GET`  | `/providers` | Modelos disponibles por proveedor |
| `GET`  | `/profiles` | System prompts preconfigurados |

`POST /chat` body mínimo:
```json
{ "message": "Me llamo Adrián", "conversation_id": null, "model": "llama3.2:3b" }
```

Respuesta: `{ conversation_id, reply, metrics: { wall_time_s, total_tokens, tokens_per_second, ... } }`.

---

## 🧠 Cómo funciona el contexto

Cada request crea o reutiliza una `conversation_id`. El backend:

1. Recupera todos los `messages` previos de esa conversación.
2. Los concatena con el system prompt y el nuevo mensaje del usuario.
3. Envía el arreglo completo a Ollama (`/api/chat`).
4. Guarda par user/assistant en SQLite.

**Demo (4 turnos en una misma conversación):**
```
1. "Me llamo Adrián y estudio ingeniería"         → "¡Hola Adrián! ..."
2. "¿Cómo me llamo?"                               → "Te llamas Adrián" ✅
3. "¿Qué lenguajes debería aprender?"               → "Python, C, JavaScript..."
4. "¿Cuál de esos es mejor para comenzar?"         → recomendación contextual ✅
```

Una conversación **nueva** no ve los mensajes de otras: `conversation_id: null` siempre inicia desde cero.

---

## 📊 Métricas (N = 40 pruebas reales)

> **Resumen de la batería.** El script `practicas/test_metrics_battery.py` ejecutó **8 escenarios × 5 repeticiones = N = 40 invocaciones medidas** a `llama3.2:3b` durante **~7 min 48 s**, todas exitosas (40/40 ok). Modelo `llama3.2:3b`, parámetros por defecto (`temperature=0.7`, `top_p=0.9`, `repeat_penalty=1.1`, `num_ctx=4096`). Los números siguientes son agregados (mean ± stdev) sobre los 5 runs de cada escenario. Datos crudos en [`assets/practica-3/metrics_summary_20260702_201335.json`](assets/practica-3/metrics_summary_20260702_201335.json).

### Tabla comparativa (N = 5 por escenario)

| Escenario | N | Wall time (s) | Prompt tok | Completion tok | Total tok | Tokens/s |
|-----------|--:|---------------:|-----------:|---------------:|----------:|---------:|
| **S1** Primer mensaje (sin historial) | 5 | 4.27 ± 0.6 | 74 | 160 ± 0 | 234 ± 0 | **39.8 ± 4.2** |
| **S2** 3.er mensaje (2 turnos previos) | 5 | 4.72 ± 0.3 | **390 ± 24** | 160 ± 0 | 550 ± 24 | 36.2 ± 2.6 |
| **S3** Respuesta técnica (código) | 5 | 15.79 ± 1.1 | 80 | **400 ± 0** | 480 ± 0 | 25.9 ± 2.0 |
| **S4** Temperatura baja (0.2) | 5 | 5.61 ± 0.3 | 74 | 160 ± 0 | 234 ± 0 | 29.6 ± 1.7 |
| **S5** Temperatura alta (1.0) | 5 | 4.87 ± 0.3 | 74 | 160 ± 0 | 234 ± 0 | 34.0 ± 1.8 |
| **S6** `max_tokens=60` | 5 | **1.76 ± 0.07** | 74 | **60 ± 0** | 134 ± 0 | 36.7 ± 1.5 |
| **S7** `max_tokens=300` | 5 | 6.45 ± 0.9 | 74 | 214 ± 29 | 288 ± 29 | 34.1 ± 0.6 |
| **S8** Turno 10 (9 turnos previos) | 5 | 5.81 ± 0.9 | **1263 ± 16** | 160 ± 0 | **1423 ± 16** | 29.5 ± 3.8 |

### Lectura de los datos

- **Velocidad estable: 25-40 tokens/s.** Es la métrica menos ruidosa (stdev entre 0.6 y 4.2). `llama3.2:3b` corre cómodo en este equipo.
- **El historial sí cuesta.** Comparar S1 vs S8: mismo `max_tokens=160` en la salida, pero prompt_tokens sube de **74 → 1263** (×17). El wall time solo sube de 4.3 s → 5.8 s (×1.4) porque la mayor parte del contexto cabe en prefill rápido; el cuello de botella sigue siendo la **generación**, no la lectura del prompt.
- **`max_tokens` corta la salida de verdad.** S6 (max=60) genera 60 tokens exactos; S7 (max=300) genera hasta 214 (no siempre llega al tope, depende de EOS); S3 (max=400) llena los 400.
- **`temperature` no afecta visiblemente ni velocidad ni longitud media** (S4=5.61 s vs S5=4.87 s, dentro de ±2σ). Su efecto es semántico (variabilidad léxica), no de costo computacional.
- **Primer run paga carga del modelo.** En escenarios sin seeding, los 5 runs son casi deterministas (stdev < 1 s). El warm-up se nota al comparar la corrida 1 vs corridas 2-5 dentro de cada escenario, pero promediando se diluye.

### Cobertura del contexto conversacional

`test_metrics_battery.py` valida cuantitativamente el efecto del historial:

| Configuración | prompt_tokens | ratio vs S1 |
|---------------|--------------:|------------:|
| Sin historial (S1) | 74 | 1.0× |
| 2 turnos previos (S2) | 390 | 5.3× |
| 9 turnos previos (S8) | 1263 | 17.1× |

Crecimiento promedio ≈ **+150 tokens por turno previo** (consistente con respuestas medias de ~75 tokens por par user+assistant, más el system prompt).

---

## 🛠️ Cómo reproducir la batería

---

## 🛠️ Cómo reproducir la batería

```bash
# 1. Arrancar Ollama con el modelo
ollama pull llama3.2:3b
ollama serve &

# 2. Arrancar backend de la práctica 3
cd practicas/backend
source .venv/bin/activate  # o crear con: python3 -m venv .venv
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8002 --reload

# 3. Correr la batería (N=5/escenario)
cd ../..
python3 practicas/test_metrics_battery.py
```

Salida esperada (resumen):
```
Total runs: 40 (ok 40)
Tiempo total bateria: ~440 s
JSON raw:    docs/assets/practica-3/metrics_raw_<TIMESTAMP>.json
JSON summary: docs/assets/practica-3/metrics_summary_<TIMESTAMP>.json
```

Para modificar `N`, editar `RUNS_PER_SCENARIO` en la línea 24 del script.

---

## 🧰 Stack

- **Backend:** FastAPI · SQLAlchemy · SQLite · Pydantic · Uvicorn · Requests · `google-genai` · `openai`
- **Frontend:** HTML5 · CSS3 (grid + flexbox) · JavaScript (fetch API) · localStorage
- **Inferencia:** Ollama local con `llama3.2:3b`

---

## 📝 Notas finales

- **Costos.** Ollama local: $0 USD por inferencia (solo costo eléctrico).
- **Cobertura del contexto.** La batería (S1/S2/S8 con prompt_tokens 74/390/1263) confirma cuantitativamente que el backend pasa el historial a Ollama turno a turno.
- **Reproducibilidad.** Los JSON raw y summary están versionados por timestamp en `docs/assets/practica-3/`; cada corrida es autocontenida.
