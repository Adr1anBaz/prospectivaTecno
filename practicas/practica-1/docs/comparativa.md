---
layout: default
title: 4. Tabla Comparativa
nav_order: 5
---

# Tabla Comparativa de Modelos LLM

Comparación de modelos ejecutados localmente con Ollama.

## Tabla de Comparación

| Modelo | Desarrollador | Tipo de Modelo | Licencia | Parámetros | Lenguajes Soportados | Requisitos Técnicos | Observaciones |
|--------|--------------|----------------|----------|------------|---------------------|---------------------|---------------|
| **Llama 3.2 3B** | Meta | Decoder-only | Llama 3.2 Community License | 3B | Multilingüe (Inglés, Español, Alemán, Francés, etc.) | ~4 GB RAM<br>Disco: ~2.0 GB<br>Inferencia muy rápida | Excelente balance velocidad/calidad para tareas generales y razonamiento en su tamaño. |
| **Gemma 2 2B** | Google | Decoder-only | Gemma Terms of Use | 2B | Multilingüe (Inglés, Español, Francés, etc.) | ~4 GB RAM<br>Disco: ~1.6 GB<br>Inferencia muy rápida | Sorprendente rendimiento en español para su tamaño; supera a modelos más grandes en lógica básica. |
| **Qwen 2.5 7B** | Alibaba | Decoder-only | Apache 2.0 | 7B | Multilingüe (Excelente soporte en Español, Inglés, Chino) | ~8 GB-16 GB RAM<br>Disco: ~4.7 GB<br>Inferencia moderada | Altamente especializado en código, matemáticas y un entendimiento del español extremadamente natural. |
| **Mistral 7B** | Mistral AI | Decoder-only | Apache 2.0 | 7B | Principalmente Inglés y Francés (Español aceptable) | ~8 GB-16 GB RAM<br>Disco: ~4.1 GB<br>Inferencia moderada | Un clásico muy sólido y eficiente, aunque superado en español por opciones más recientes como Qwen. |
| **Phi-4** | Microsoft | Decoder-only | MIT | 14B | Multilingüe (Principalmente Inglés, Español bueno) | ~16 GB RAM (Mínimo)<br>GPU recomendada<br>Disco: ~9.1 GB<br>Inferencia lenta en CPU | El más pesado del grupo; capacidades de razonamiento lógico, científico y técnico de nivel superior. |
| **TinyLlama** | TinyLlama Project | Decoder-only | Apache 2.0 | 1.1B | Principalmente Inglés (Español muy limitado/deficiente) | ~2 GB RAM<br>Disco: ~640 MB<br>Inferencia ultra rápida | Ideal para dispositivos ultra-limitados, pero sufre de alucinaciones frecuentes y baja coherencia en español. |

*Nota: Los tamaños de disco corresponden a los modelos cuantizados por defecto (`q4_K_M`) que descarga la librería de Ollama de forma nativa.*

## Instrucciones de Llenado

Para cada modelo, consulta su página en Hugging Face y completa:

### Desarrollador
Empresa o institución que creó el modelo (ej: Meta, Google, Alibaba, Microsoft)

### Tipo de Modelo
Arquitectura del modelo:
- Decoder-only (GPT-style)
- Encoder-decoder (T5-style)
- Encoder-only (BERT-style)

### Licencia
Tipo de licencia (ej: Apache 2.0, MIT, Llama 3 License, GPL)

### Parámetros
Número de parámetros del modelo (ya está completado)

### Lenguajes Soportados
Lista de idiomas que el modelo maneja bien (ej: Inglés, Español, Multilingüe)

### Requisitos Técnicos
- RAM mínima requerida
- GPU recomendada (si aplica)
- Espacio en disco para el modelo
- Tiempo aproximado de inferencia

### Observaciones
Notas adicionales:
- Especialización del modelo (ej: código, chat, instrucciones)
- Peculiaridades en su uso
- Comparación de velocidad/calidad respecto a otros modelos

## Ejemplo de Fuentes

Para encontrar esta información, busca en:

1. **Hugging Face:**
   - `https://huggingface.co/meta-llama/Llama-3.2-3B`
   - `https://huggingface.co/google/gemma-2-2b`
   - etc.

2. **Ollama Library:**
   - `https://ollama.com/library/llama3.2`
   - Comando: `ollama show llama3.2:3b`

3. **Repositorios oficiales:**
   - GitHub del desarrollador
   - Páginas de documentación oficial

## Análisis Comparativo

Después de completar la tabla, responde:

### 1. ¿Qué modelo tuvo mejor desempeño en español?
**Qwen 2.5 7B** y **Llama 3.2 3B**. Qwen 2.5 cuenta con un vocabulario y entrenamiento multilingüe masivo que le permite redactar con una gramática, fluidez y modismos en español excelentes. Por su parte, Llama 3.2 3B ofrece una comprensión del español sobresaliente considerando su reducido tamaño.

### 2. ¿Hay relación entre número de parámetros y calidad de respuesta?
Sí, existe una correlación directa. A mayor número de parámetros (como **Phi-4** con 14B o **Qwen 2.5** con 7B), el modelo posee una mayor capacidad de abstracción, retención de contexto y precisión lógica. Sin embargo, arquitecturas más optimizadas y recientes (como **Gemma 2 2B**) logran demostrar que un modelo pequeño bien entrenado puede superar la calidad de modelos más antiguos de 7B en tareas comunes.

### 3. ¿Qué modelo fue más rápido? ¿Por qué?
**TinyLlama (1.1B)**, seguido muy de cerca por **Gemma 2 2B** y **Llama 3.2 3B**. La velocidad de inferencia (tokens por segundo) es inversamente proporcional al tamaño del modelo: al requerir menos operaciones matemáticas por cada token generado y ocupar menos espacio en la memoria RAM/VRAM, el procesador (CPU/GPU) puede calcular las matrices de la arquitectura de forma mucho más ágil.

### 4. ¿Qué licencias son más permisivas para uso comercial?
Las licencias **Apache 2.0** (Qwen 2.5, Mistral 7B, TinyLlama) y **MIT** (Phi-4). Ambas son licencias de código abierto de tipo *permisivo*, lo que significa que permiten la modificación, distribución y explotación comercial del modelo de forma gratuita sin apenas restricciones. Las licencias de Meta (Llama 3.2) y Google (Gemma 2), aunque permiten el uso comercial, añaden cláusulas corporativas específicas (como límites de usuarios activos mensuales).

### 5. ¿Cuál modelo recomendarías para cada caso de uso?
- **Chatbot en español:** **Qwen 2.5 7B** por su excelente riqueza lingüística, o **Llama 3.2 3B** si se busca un menor consumo de recursos manteniendo coherencia.
- **Aplicación móvil (recursos limitados):** **Gemma 2 2B** o **Llama 3.2 3B**, ya que ofrecen un rendimiento lingüístico real ocupando menos de 2 GB de espacio en disco.
- **Investigación académica:** **Phi-4 (14B)**, debido a su avanzado entrenamiento en razonamiento complejo y resolución de problemas técnicos estructurados.
- **Producción comercial:** **Qwen 2.5 7B** o **Mistral 7B** por la flexibilidad y seguridad legal que otorga la licencia Apache 2.0 junto con su gran robustez.

---

**Fecha de elaboración:** 1 de junio de 2026  
**Autor:** Adrian Bazaldua