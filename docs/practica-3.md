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

[Ver en GitHub](https://github.com/Adr1anBaz/prospectivaTecno/tree/main/practicas/practica-3){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 }

---

## 📋 Información General

| Campo | Detalle |
|:------|:--------|
| **Alumnos** | Adrián Bazaldua, Fernando Pérez, Sebastián Enguilo |
| **Fecha** | Julio 2026 |
| **Práctica** | #3 - Chatbot con Contexto y Base de Datos |
| **Modelo** | `llama3.2:3b` (Q4_K_M, 2.0 GB) vía Ollama local |
| **Backend** | FastAPI en `127.0.0.1:8000` |
| **Frontend** | HTML/CSS/JS en `localhost:5500` |

---

## 🎯 Características

- Contexto conversacional persistente por conversación (SQLite)
- API REST: crear / listar / obtener / eliminar conversaciones
- Métricas por respuesta: wall time, tokens entrada/salida, velocidad
- Configuración de parámetros desde el frontend (`temperature`, `top_p`, `num_predict`, `num_ctx`, `repeat_penalty`)
- Solo Ollama local (sin proveedores externos)

---

## 📐 Arquitectura

```
Usuario → Frontend (HTML/JS, puerto 5500)
        → Backend FastAPI (puerto 8000)
            → recupera historial de SQLite
            → llama a Ollama (puerto 11434) con messages[]
            → guarda par user/assistant en SQLite
        ← JSON { conversation_id, reply, metrics }
```

El navegador **nunca** habla directo con Ollama: el backend valida, mide y estructura la respuesta.

---

## 🗂️ Estructura

```
practicas/practica-3/
├── backend/
│   ├── main.py              # FastAPI: /, /health, /chat, /conversations
│   ├── database.py          # SQLAlchemy (conversations, messages)
│   ├── chatbot.db           # SQLite (generado)
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js               # mantiene conversation_id para el contexto
├── test_metrics_battery.py  # batería de métricas (este doc la usa)
└── README.md
```

Los JSON crudos y el resumen de la batería se guardan en `docs/assets/practica-3/`.

---

## 🔌 API esencial

| Método | Endpoint | Uso |
|--------|----------|-----|
| `POST` | `/chat` | Enviar mensaje; recibe `conversation_id` |
| `GET`  | `/conversations` | Listar conversaciones |
| `GET`  | `/conversations/{id}` | Obtener historial |
| `DELETE` | `/conversations/{id}` | Borrar conversación |
| `GET`  | `/health` | Estado del backend |

`POST /chat` body mínimo:
```json
{ "message": "Me llamo Adrián", "conversation_id": null, "model": "llama3.2:3b" }
```

Respuesta: `{ conversation_id, model, reply, metrics: { wall_time_s, total_tokens, tokens_per_second, ... } }`.

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

> **Resumen de la batería.** El script `practicas/practica-3/test_metrics_battery.py` ejecutó **8 escenarios × 5 repeticiones = N = 40 invocaciones medidas** a `llama3.2:3b` durante **~7 min 35 s**, todas exitosas (40/40 ok). Backend en `127.0.0.1:8000`, parámetros por defecto (`temperature=0.7`, `top_p=0.9`, `repeat_penalty=1.1`, `num_ctx=4096`). Los números siguientes son agregados (mean ± stdev) sobre los 5 runs de cada escenario. Datos crudos en [`assets/practica-3/metrics_summary_20260702_230248.json`](assets/practica-3/metrics_summary_20260702_230248.json).

### Tabla comparativa (N = 5 por escenario)

| Escenario | N | Wall time (s) | Prompt tok | Completion tok | Total tok | Tokens/s |
|-----------|--:|---------------:|-----------:|---------------:|----------:|---------:|
| **S1** Primer mensaje (sin historial) | 5 | 4.66 ± 0.39 | 56 | 160 ± 0 | 216 ± 0 | **36.98 ± 0.09** |
| **S2** 3.er mensaje (2 turnos previos) | 5 | 4.74 ± 0.08 | **373 ± 33** | 160 ± 0 | 533 ± 33 | 35.34 ± 0.52 |
| **S3** Respuesta técnica (código) | 5 | 11.28 ± 0.10 | 62 | **400 ± 0** | 462 ± 0 | 36.31 ± 0.19 |
| **S4** Temperatura baja (0.2) | 5 | 4.63 ± 0.12 | 56 | 160 ± 0 | 216 ± 0 | 35.98 ± 0.66 |
| **S5** Temperatura alta (1.0) | 5 | 4.55 ± 0.06 | 56 | 158 ± 4 | 214 ± 4 | 36.09 ± 0.22 |
| **S6** `num_predict=60` | 5 | **1.82 ± 0.05** | 56 | **60 ± 0** | 116 ± 0 | 35.54 ± 0.65 |
| **S7** `num_predict=300` | 5 | 6.59 ± 0.90 | 56 | 221 ± 32 | 277 ± 32 | 34.47 ± 0.47 |
| **S8** Turno 10 (9 turnos previos) | 5 | 6.12 ± 0.19 | **1275 ± 23** | 160 ± 0 | **1435 ± 23** | 27.39 ± 0.83 |

### Lectura de los datos

- **Velocidad estable: 27-37 tokens/s.** Es la métrica menos ruidosa (stdev entre 0.09 y 0.83). `llama3.2:3b` corre cómodo en este equipo.
- **El historial sí cuesta.** Comparar S1 vs S8: mismo `num_predict=160` en la salida, pero prompt_tokens sube de **56 → 1275** (×22.8). El wall time solo sube de 4.66 s → 6.12 s (×1.3) porque el prefill del contexto es rápido; aun así, `tokens_per_second` cae de **37.0 → 27.4** en el turno con más historial.
- **`num_predict` corta la salida de verdad.** S6 (=60) genera 60 tokens exactos; S7 (=300) genera hasta ~221 en promedio (no siempre llega al tope, depende de EOS); S3 (=400) llena los 400.
- **`temperature` no afecta visiblemente ni velocidad ni longitud media** (S4=4.63 s vs S5=4.55 s, dentro de ±2σ). Su efecto es semántico (variabilidad léxica), no de costo computacional.
- **Primer run paga carga del modelo.** En escenarios sin seeding, los 5 runs son casi deterministas (stdev < 0.4 s); S1 es el de mayor dispersión por el warm-up de la primera corrida.

### Cobertura del contexto conversacional

`test_metrics_battery.py` valida cuantitativamente el efecto del historial:

| Configuración | prompt_tokens | ratio vs S1 |
|---------------|--------------:|------------:|
| Sin historial (S1) | 56 | 1.0× |
| 2 turnos previos (S2) | 373 | 6.7× |
| 9 turnos previos (S8) | 1275 | 22.8× |

Crecimiento promedio ≈ **+135 tokens por turno previo** (consistente con respuestas medias de ~75 tokens por par user+assistant, más el system prompt).

---

## 🛠️ Cómo reproducir la batería

```bash
# 1. Arrancar Ollama con el modelo
ollama pull llama3.2:3b
ollama serve &

# 2. Arrancar backend de la práctica 3
cd practicas/practica-3/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# 3. Correr la batería (N=5/escenario) desde la raíz del repo
cd ../../..
python3 practicas/practica-3/test_metrics_battery.py
```

Salida esperada (resumen):
```
Total runs: 40 (ok 40)
Tiempo total bateria: ~455 s
JSON raw:    docs/assets/practica-3/metrics_raw_<TIMESTAMP>.json
JSON summary: docs/assets/practica-3/metrics_summary_<TIMESTAMP>.json
```

Para modificar `N`, editar la constante `RUNS_PER_SCENARIO` en el script.

---

## 🧰 Stack

- **Backend:** FastAPI · SQLAlchemy · SQLite · Pydantic · Uvicorn · Requests
- **Frontend:** HTML5 · CSS3 (grid + flexbox) · JavaScript (fetch API) · estado en memoria (`conversation_id`)
- **Inferencia:** Ollama local con `llama3.2:3b`

---

## Reflexión técnica

1. **¿Qué modelo local utilizaste?** `llama3.2:3b` (Q4_K_M, 2.0 GB) vía Ollama. El selector del frontend también ofrece los otros modelos instalados (`qwen2.5:3b`, `qwen2.5:1.5b`, `llama3.2:1b`, `qwen2.5:0.5b`) como alternativas más ligeras.
2. **¿Qué parámetros configuraste desde el frontend?** `model`, `temperature`, `top_p`, `num_predict`, `num_ctx` y `repeat_penalty`. El backend valida sus rangos con Pydantic antes de llamar a Ollama.
3. **¿Qué ocurre al aumentar `num_predict`?** La salida se alarga y el wall time crece casi linealmente: S6 (60 tok) = 1.82 s, S7 (300 tok) = 6.59 s, S3 (400 tok) = 11.28 s. La velocidad se mantiene estable (~34–37 tok/s): `num_predict` cambia *cuántos* tokens se generan, no *qué tan rápido*.
4. **¿Qué ocurre al modificar `temperature`?** No afecta velocidad ni longitud media (S4 con 0.2 = 4.63 s vs S5 con 1.0 = 4.55 s, dentro del ruido). Su efecto es semántico: mayor temperatura = más variabilidad léxica y creatividad, menor = respuestas más deterministas.
5. **¿Por qué es útil mostrar tokens y latencia?** Dan transparencia del costo y desempeño real. Por ejemplo, permiten ver el costo del contexto (prompt_tokens sube de 56 a 1275 al acumular historial) y decidir cuándo conviene limpiar la conversación o bajar `num_predict`.
6. **¿Por qué usar backend en vez de conectar el navegador directo a Ollama?** El backend valida parámetros, gestiona CORS, mide métricas de forma consistente, mantiene el contexto en SQLite, maneja errores (503/504/500) y evita exponer Ollama directamente al cliente.
7. **¿Cómo extenderías este chatbot para tu proyecto?** Con recuperación aumentada (RAG) sobre documentos propios, autenticación de usuarios, respuesta en streaming, soporte de más proveedores/modelos y, en el contexto de robótica, una capa intermedia de validación antes de traducir respuestas del LLM en acciones físicas.

---

## Capturas (entregable del reporte)

> Pendientes de adjuntar por el equipo:
> - Ollama con el modelo instalado (`ollama list`).
> - Backend ejecutándose (`uvicorn` en el puerto 8000 / `/docs`).
> - Prueba del endpoint `/chat` (curl o Swagger `/docs`).
> - Frontend funcionando (conversación con contexto).
> - Panel de métricas visibles tras una respuesta.

---

## 📝 Notas finales

- **Costos.** Ollama local: $0 USD por inferencia (solo costo eléctrico).
- **Cobertura del contexto.** La batería (S1/S2/S8 con prompt_tokens 56/373/1275) confirma cuantitativamente que el backend pasa el historial a Ollama turno a turno.
- **Reproducibilidad.** Los JSON raw y summary están versionados por timestamp en `docs/assets/practica-3/`; cada corrida es autocontenida.
