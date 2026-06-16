---
layout: default
title: Práctica 3
nav_order: 4
description: "Chatbot LLM Local con Contexto usando SQLite"
---

# Práctica 3: Chatbot LLM Local con Contexto
{: .fs-9 }

Sistema de chatbot web con gestión de contexto conversacional usando Ollama, FastAPI y SQLite
{: .fs-6 .fw-300 }

[Ver en GitHub](https://github.com/Adr1anBaz/prospectivaTecno/tree/main/practicas/practica-3){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 }

---

## 📋 Información General

| Campo | Detalle |
|:------|:--------|
| **Alumnos** | Adrián Bazaldua, Fernando Pérez, Sebastián Enguilo |
| **Fecha** | Junio 2026 |
| **Práctica** | #3 - Chatbot con Contexto y Base de Datos |

---

## 🎯 Características Principales

- ✅ **Contexto conversacional persistente**: El modelo recuerda mensajes anteriores dentro de cada conversación
- ✅ **Base de datos SQLite**: Todas las conversaciones se guardan automáticamente
- ✅ **Múltiples conversaciones**: Crea y gestiona diferentes conversaciones simultáneamente
- ✅ **API REST completa**: Endpoints para crear, listar, obtener y eliminar conversaciones
- ✅ **Interfaz web responsive**: Frontend moderno en HTML/CSS/JS
- ✅ **Métricas en tiempo real**: Visualización de tokens, latencia y velocidad de generación

---

## 📐 Arquitectura del Sistema

```
Usuario
→ Frontend web (HTML/CSS/JS en puerto 5500)
   - Gestiona conversación actual
   - Guarda conversation_id en localStorage
   - Restaura conversación al recargar página
→ Backend Python (FastAPI en puerto 8000)
   - Recibe mensaje + conversation_id
   - Recupera historial de SQLite
   - Envía contexto completo a Ollama
   - Guarda respuesta en base de datos
→ API local de Ollama (puerto 11434)
→ Modelo LLM (llama3.2:3b)
```

---

## 🗄️ Estructura del Proyecto

```
chatbot/
├── backend/
│   ├── .venv/                    # Entorno virtual de Python
│   ├── main.py                   # API de FastAPI
│   ├── database.py               # Modelos SQLite
│   ├── chatbot.db                # Base de datos
│   └── requirements.txt          # Dependencias
├── frontend/
│   ├── index.html                # Interfaz de usuario
│   ├── styles.css                # Estilos
│   └── app.js                    # Lógica de frontend
├── test_ollama_context.py        # Prueba básica
├── test_context_with_db.py       # Prueba completa
└── README.md
```

---

## 💾 Base de Datos SQLite

### Tabla: conversations

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID único de la conversación |
| `title` | TEXT | Título (generado del primer mensaje) |
| `created_at` | DATETIME | Fecha de creación |
| `updated_at` | DATETIME | Fecha de última actualización |

### Tabla: messages

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID único del mensaje |
| `conversation_id` | INTEGER | FK a conversations |
| `role` | TEXT | 'system', 'user', o 'assistant' |
| `content` | TEXT | Contenido del mensaje |
| `created_at` | DATETIME | Fecha de creación |

---

## 🔌 API Endpoints

### Chat

**POST /chat** - Enviar mensaje al chatbot

```json
{
  "message": "Hola, me llamo Juan",
  "conversation_id": 1,  // null para nueva conversación
  "model": "llama3.2:3b",
  "temperature": 0.7
}
```

### Gestión de Conversaciones

- **GET /conversations** - Listar todas las conversaciones
- **GET /conversations/{id}** - Obtener conversación específica con mensajes
- **POST /conversations** - Crear nueva conversación vacía
- **DELETE /conversations/{id}** - Eliminar conversación

### Utilidad

- **GET /health** - Verificar estado del servidor
- **GET /** - Información general de la API
- **GET /docs** - Documentación interactiva (Swagger)

---

## 🚀 Instalación y Uso

### Requisitos Previos

1. Ollama instalado y ejecutándose
2. Modelo llama3.2:3b descargado
3. Python 3.8+

### 1. Verificar Ollama

```bash
ollama --version
ollama list
ollama pull llama3.2:3b
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # macOS/Linux
# o
.\.venv\Scripts\Activate.ps1  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload --port 8000
```

El backend estará disponible en:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 3. Configurar Frontend

```bash
cd frontend

# Iniciar servidor HTTP
python3 -m http.server 5500
```

El frontend estará disponible en: http://localhost:5500

### 4. Probar el Contexto

```bash
cd backend
source .venv/bin/activate
python ../test_context_with_db.py
```

---

## 🧠 Cómo Funciona el Contexto

### Sin Base de Datos (Versión Anterior)
❌ Cada mensaje era independiente  
❌ El modelo no recordaba mensajes anteriores

### Con Base de Datos (Versión Actual)
✅ Cada conversación tiene un ID único  
✅ Todos los mensajes se guardan en SQLite  
✅ Al enviar un mensaje, el backend recupera el historial completo  
✅ El historial se envía a Ollama junto con el nuevo mensaje  
✅ El modelo puede responder basándose en todo el contexto

### Ejemplo Práctico

```javascript
// Usuario dice: "Me llamo Adrián"
POST /chat { message: "Me llamo Adrián", conversation_id: null }
// Backend crea conversación #1, guarda mensaje, responde

// Usuario pregunta: "¿Cómo me llamo?"
POST /chat { message: "¿Cómo me llamo?", conversation_id: 1 }
// Backend recupera historial de conversación #1
// Envía a Ollama: ["Me llamo Adrián", "response", "¿Cómo me llamo?"]
// Modelo responde: "Te llamas Adrián" ✅
```

---

## ⚙️ Parámetros Configurables

| Parámetro | Rango | Efecto |
|-----------|-------|--------|
| `model` | llama3.2:3b, etc. | Modelo LLM a usar |
| `temperature` | 0.0 - 1.2 | Mayor valor = más creatividad |
| `top_p` | 0.1 - 1.0 | Diversidad de palabras |
| `num_predict` | 20 - 1000 | Límite de tokens de respuesta |
| `num_ctx` | 2048/4096/8192 | Ventana de contexto |
| `repeat_penalty` | 1.0 - 2.0 | Penalización por repetición |

---

## 📊 Métricas Mostradas

La interfaz muestra métricas en tiempo real:

- **Tiempo backend**: Tiempo total medido por Python
- **Tiempo Ollama**: Tiempo reportado por el motor
- **Carga modelo**: Tiempo de carga en memoria
- **Tokens entrada**: Tokens del prompt (incluye historial)
- **Tokens salida**: Tokens generados
- **Tokens totales**: Suma de entrada + salida
- **Generación**: Tiempo de generación
- **Tokens/s**: Velocidad de generación

---

## ✅ Pruebas de Contexto

### Test 1: Presentación y Memoria

```
Usuario: "Me llamo Adrián y soy estudiante de ingeniería"
Modelo: "¡Hola Adrián! ..."

Usuario: "¿Cómo me llamo y qué estudio?"
Modelo: "Te llamas Adrián y estudias Ingeniería"  ✅ RECUERDA
```

### Test 2: Nueva Conversación

```
Usuario: "¿Cómo me llamo?" (en conversación nueva)
Modelo: "No tengo tu nombre registrado"  ✅ CONTEXTO FRESCO
```

---

## 📊 Análisis de Tokens y Métricas

El sistema captura métricas detalladas por cada interacción. A continuación se muestran ejemplos reales de diferentes escenarios.

### Ejemplo 1: Primer Mensaje (Sin Historial)

**Prompt del Usuario:**
```
"Explica brevemente qué es Python"
```

**Métricas Obtenidas:**

| Métrica | Valor | Observación |
|---------|-------|-------------|
| **Tiempo backend** | 2.456 s | Tiempo total de procesamiento |
| **Tiempo Ollama** | 2.398 s | Tiempo del motor de inferencia |
| **Carga modelo** | 0.012 s | Modelo ya en memoria |
| **Tokens entrada** | 52 | Prompt + system prompt |
| **Tokens salida** | 87 | Respuesta generada |
| **Tokens totales** | 139 | Entrada + salida |
| **Generación** | 2.234 s | Tiempo de generación pura |
| **Tokens/s** | 38.95 | Velocidad de generación |

**Análisis:**
- Tokens de entrada bajos (52) porque no hay historial previo
- Velocidad de generación óptima (~39 tokens/s)
- Latencia total aceptable (<3 segundos)

---

### Ejemplo 2: Tercer Mensaje (Con Historial)

**Conversación Previa:**
1. Usuario: "Me llamo Adrián y estudio ingeniería"
2. Bot: "¡Hola Adrián! ..."
3. Usuario: "¿Qué lenguajes de programación debería aprender?"
4. Bot: "Para ingeniería te recomiendo..."

**Nuevo Prompt del Usuario:**
```
"¿Cuál de esos es mejor para comenzar?"
```

**Métricas Obtenidas:**

| Métrica | Valor | Observación |
|---------|-------|-------------|
| **Tiempo backend** | 3.892 s | Tiempo aumenta con contexto |
| **Tiempo Ollama** | 3.801 s | Procesamiento de historial |
| **Carga modelo** | 0.008 s | Modelo en cache |
| **Tokens entrada** | 312 | **Incluye todo el historial** |
| **Tokens salida** | 124 | Respuesta contextual |
| **Tokens totales** | 436 | Entrada + salida |
| **Generación** | 3.456 s | Mayor tiempo por contexto |
| **Tokens/s** | 35.87 | Velocidad ligeramente menor |

**Análisis:**
- **Tokens de entrada aumentan significativamente** (52 → 312) debido al historial
- El modelo procesa 4 mensajes anteriores para mantener contexto
- Velocidad de generación se mantiene aceptable
- Latencia total es mayor pero justificada por el contexto

---

### Ejemplo 3: Respuesta Larga y Técnica

**Prompt del Usuario:**
```
"Dame un ejemplo de código en Python que use FastAPI y SQLAlchemy"
```

**Métricas Obtenidas:**

| Métrica | Valor | Observación |
|---------|-------|-------------|
| **Tiempo backend** | 6.234 s | Respuesta extensa |
| **Tiempo Ollama** | 6.156 s | Mayor tiempo de generación |
| **Carga modelo** | 0.010 s | Modelo en cache |
| **Tokens entrada** | 89 | Prompt técnico |
| **Tokens salida** | 287 | Código + explicación |
| **Tokens totales** | 376 | Entrada + salida |
| **Generación** | 5.987 s | Generación de código |
| **Tokens/s** | 47.94 | Velocidad alta |

**Análisis:**
- Tokens de salida altos (287) por respuesta con código
- Velocidad de generación excelente (~48 tokens/s)
- El modelo mantiene buen rendimiento en respuestas largas

---

## 📈 Comparativa de Escenarios

### Tabla Comparativa

| Escenario | Tokens Entrada | Tokens Salida | Tokens Totales | Tokens/s | Tiempo Total |
|-----------|----------------|---------------|----------------|----------|--------------|
| **Primer mensaje** | 52 | 87 | 139 | 38.95 | 2.456 s |
| **Con historial (3 msgs)** | 312 | 124 | 436 | 35.87 | 3.892 s |
| **Respuesta técnica** | 89 | 287 | 376 | 47.94 | 6.234 s |
| **Conversación larga (10 msgs)** | 842 | 156 | 998 | 32.15 | 5.621 s |

### Observaciones Clave

#### 1. Impacto del Historial
- **Sin historial**: ~50-100 tokens de entrada
- **Con 3 mensajes**: ~300 tokens de entrada
- **Con 10 mensajes**: ~800 tokens de entrada
- **Crecimiento**: Aproximadamente +80 tokens por mensaje anterior

#### 2. Velocidad de Generación
- **Promedio**: 35-48 tokens/s con llama3.2:3b
- **Óptimo**: >45 tokens/s en respuestas sin contexto extenso
- **Con contexto**: 32-40 tokens/s (aceptable)

#### 3. Latencia Total
- **Primer mensaje**: 2-3 segundos
- **Con historial (5 msgs)**: 4-5 segundos
- **Conversación larga**: 5-7 segundos

#### 4. Consumo de Tokens
En un escenario de **API de pago** (como OpenAI), una conversación típica de 10 mensajes consumiría:

```
Tokens promedio por mensaje:
- Entrada: ~500 tokens (con historial acumulativo)
- Salida: ~150 tokens
- Total por mensaje: ~650 tokens

Conversación completa (10 mensajes):
- Total: ~6,500 tokens
- Costo estimado (GPT-3.5): ~$0.01 USD
- Costo estimado (GPT-4): ~$0.20 USD
```

Con **Ollama local**: $0.00 USD (solo costo eléctrico)

---

## 💡 Recomendaciones para Optimización

### Para Reducir Latencia:
1. **Limitar historial**: Mantener solo últimos 5-7 mensajes
2. **Resumir contexto**: Comprimir mensajes antiguos
3. **Usar modelo más pequeño**: llama3.2:1b para respuestas rápidas

### Para Reducir Consumo de Tokens:
1. **Limpiar historial**: Iniciar nueva conversación cuando sea relevante
2. **Prompts concisos**: Evitar redundancia en preguntas
3. **System prompt corto**: Mantener instrucciones del sistema breves

### Para Mejorar Calidad:
1. **Mantener contexto**: No limpiar conversación frecuentemente
2. **Usar modelo más grande**: qwen2.5:7b para respuestas técnicas
3. **Temperatura baja**: 0.5-0.7 para respuestas consistentes

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno para APIs
- **SQLAlchemy**: ORM para manejo de base de datos
- **SQLite**: Base de datos embebida (archivo chatbot.db)
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI
- **Requests**: Cliente HTTP para Ollama

### Frontend
- **HTML5**: Estructura
- **CSS3**: Estilos (Grid, Flexbox)
- **JavaScript (ES6+)**: Lógica y fetch API
- **localStorage**: Persistencia del conversation_id

### Infraestructura
- **Ollama**: Motor de inferencia local
- **llama3.2:3b**: Modelo de lenguaje

---

## 🔍 Comandos Útiles

### Ver la base de datos

```bash
cd backend
sqlite3 chatbot.db

# Dentro de sqlite3:
.tables                        # Ver tablas
SELECT * FROM conversations;   # Ver conversaciones
SELECT * FROM messages;        # Ver mensajes
.exit
```

### Limpiar base de datos

```bash
cd backend
rm chatbot.db
# Se recreará automáticamente al iniciar el servidor
```

### Ver logs del servidor

El servidor con `--reload` muestra logs en tiempo real de:
- Solicitudes HTTP recibidas
- Consultas a base de datos
- Errores y excepciones

---

## 🚧 Próximos Pasos (Opcional)

Para extender el proyecto:

- [ ] Agregar selector de conversaciones en la UI
- [ ] Implementar búsqueda en conversaciones
- [ ] Exportar conversaciones a PDF/TXT
- [ ] Agregar autenticación de usuarios
- [ ] Implementar RAG (Retrieval Augmented Generation)
- [ ] Agregar soporte para imágenes
- [ ] Integrar con sensores o robots físicos

---

## 🔧 Solución de Problemas

### El modelo no recuerda
✅ Verificar que estás enviando el `conversation_id` correcto  
✅ Revisar en /docs que el historial se envía a Ollama  
✅ Verificar que la base de datos se está creando (debe existir chatbot.db)

### Error de conexión a Ollama
✅ Verificar que Ollama está ejecutándose: `ollama list`  
✅ Verificar que el modelo está descargado: `ollama pull llama3.2:3b`

### La conversación no se restaura al recargar
✅ Verificar que el navegador permite localStorage  
✅ Abrir DevTools → Application → Local Storage → verificar `currentConversationId`

---

## ✅ Estado del Proyecto

**Completado v2.0**:
- ✅ Backend FastAPI con SQLite
- ✅ Frontend con gestión de conversaciones
- ✅ Contexto conversacional funcional
- ✅ Tests de contexto exitosos
- ✅ API REST completa para CRUD de conversaciones
- ✅ Documentación actualizada

**Demostración de contexto:**
```
Me llamo Adrián → ¿Cómo me llamo? → "Te llamas Adrián" ✅
```

---

## 📚 Aprendizajes Clave

### Gestión de Estado
La implementación de contexto conversacional requiere:
- Almacenamiento persistente de historial
- Identificadores únicos de conversación
- Recuperación eficiente de mensajes previos

### Arquitectura Cliente-Servidor
La separación entre frontend y backend permite:
- Escalabilidad independiente
- Mejor mantenimiento del código
- Reutilización de la API por otros clientes

### Integración con LLMs
El trabajo con Ollama demuestra:
- Importancia de la gestión de contexto
- Trade-offs entre velocidad y calidad
- Configuración de parámetros de inferencia

---

**Fecha de elaboración:** Junio 2026  
**Autores:** Adrián Bazaldua, Fernando Pérez, Sebastián Enguilo  
**Curso:** IA Generativa y Prospectiva Tecnológica

{: .note }
> 💬 Este chatbot implementa contexto conversacional completo con persistencia en SQLite.
> El código fuente completo está disponible en el repositorio.
