---
layout: default
title: Inicio
nav_order: 1
description: "Repositorio de Prácticas - IA Generativa y Prospectiva Tecnológica"
permalink: /
---

# Prácticas - IA Generativa y Prospectiva Tecnológica
{: .fs-9 }

Colección de prácticas del curso de IA Generativa y Prospectiva Tecnológica: exploración de LLMs, benchmarking, chatbots locales con contexto, copilotos especializados, integración con APIs externas y una arquitectura LLM + MQTT.
{: .fs-6 .fw-300 }

[Ver en GitHub](https://github.com/Adr1anBaz/prospectivaTecno){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }

---

## Información del equipo

| Campo | Detalle |
|:------|:--------|
| **Alumnos** | Adrián Bazaldua, Fernando Pérez, Sebastián Enguilo |
| **Curso** | IA Generativa y Prospectiva Tecnológica |
| **Periodo** | Verano 2026 |

---

## Prácticas

### [Práctica 1: Panorama de IA Generativa y LLM](./practica-1)
Exploración práctica de modelos de lenguaje grande (LLM) con Ollama y Hugging Face. Instalación, descarga y ejecución de al menos 6 modelos con el mismo prompt, y comparativa documentada de su desempeño.

**Temas**: Ollama, Hugging Face, LLMs, comparativa de modelos.

---

### [Práctica 2: Selección de plataforma y benchmark de LLMs](./practica-2)
Matriz de decisión de plataformas de despliegue (PC local CPU/GPU, API en la nube, servidor GPU, Jetson, microcontrolador + API) y benchmark de modelos locales (100 ciclos por modelo) con tiempos, tokens y tokens/s reales.

**Temas**: matriz de decisión, benchmark, latencia, tokens/s.

---

### [Práctica 3: Chatbot LLM local con contexto (SQLite)](./practica-3)
Chatbot cliente-servidor (frontend HTML/CSS/JS + backend FastAPI + Ollama) con **contexto conversacional persistente en SQLite**, parámetros configurables y métricas de inferencia por respuesta.

**Temas**: FastAPI, Ollama, contexto conversacional, SQLite, métricas.

---

### [Práctica 4: Copilotos especializados con Ollama](./practica-4)
Conversión del chatbot en un copiloto especializado mediante **perfiles de `system_prompt`** seleccionables y editables, con prompting estructurado y evaluación crítica genérico vs. especializado (calidad, formato, alucinaciones, latencia).

**Temas**: prompt engineering, perfiles de copiloto, evaluación cualitativa.

---

### [Práctica 5: Chatbot híbrido con Ollama y APIs externas](./practica-5)
Capa intermedia **multiproveedor** que compara un modelo local (Ollama) con modelos remotos (Google Gemini, Groq y OpenRouter). Selección de proveedor y modelo, métricas normalizadas y comparación de latencia, tokens y calidad con el mismo prompt.

**Temas**: APIs externas, Gemini, Groq, OpenRouter, comparativa de proveedores.

---

### [Práctica 6: Evaluación de arquitectura LLM + MQTT](./practica-6)
Clasificación de intención (`on` / `off` / `none`) sobre instrucciones en español, con validación de JSON y **publicación en MQTT** como salida simulada. Incluye métricas de clasificación (precision/recall/F1), de arquitectura (validez de JSON, tasa de publicación) y de operación (latencia, tokens, costo).

**Temas**: clasificación de intención, JSON estructurado, MQTT, guardarraíles.

---

## Proyecto final

**Robot-Guided Navigation Through Conversational AI**: navegación guiada por robot mediante IA conversacional. El planteamiento teórico se presenta en un pitch deck (`proyecto-final/slides`, "Blu — Slides").

---

## Navegación

Usa el **menú lateral** para acceder a cada práctica. Cada página es autocontenida e incluye objetivo, arquitectura, resultados y análisis.

---

{: .note }
> Este sitio reúne todo el material práctico del curso. Cada práctica incluye instrucciones, código fuente, resultados y análisis. El código vive en la carpeta `practicas/` del repositorio.
