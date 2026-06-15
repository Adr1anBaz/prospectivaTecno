# Chatbot LLM Local con Ollama + SQLite + Perfiles de Copiloto

Este proyecto implementa un chatbot web con arquitectura cliente-servidor que permite conversar con un modelo LLM local mediante Ollama. **Incluye gestión de contexto conversacional usando SQLite para mantener el historial de todas las conversaciones y un sistema de perfiles de copiloto especializado con system prompts configurables.**

## 🎯 Características Principales

### Core
- ✅ **Contexto conversacional persistente**: El modelo recuerda mensajes anteriores dentro de cada conversación
- ✅ **Base de datos SQLite**: Todas las conversaciones se guardan automáticamente
- ✅ **Múltiples conversaciones**: Crea y gestiona diferentes conversaciones simultáneamente
- ✅ **API REST completa**: Endpoints para crear, listar, obtener y eliminar conversaciones

### Perfiles de Copiloto (Nuevo)
- ✅ **5 perfiles especializados**: Genérico, Docente, Robótica, Programación, Investigación
- ✅ **System prompts editables**: Personaliza el comportamiento del copiloto en tiempo real
- ✅ **Endpoint /profiles**: API para gestionar perfiles disponibles
- ✅ **Persistencia de perfil**: Cada conversación guarda qué perfil se usó

### Interfaz
- ✅ **UI moderna y responsive**: Frontend profesional con tema oscuro
- ✅ **Indicadores visuales de perfil**: Badge animado, barra de estado y nombre en mensajes
- ✅ **Métricas en modal**: Botón flotante para ver estadísticas sin bloquear el chat
- ✅ **Envío con Enter**: Presiona Enter para enviar, Shift+Enter para nueva línea
- ✅ **Formulario fijo**: Caja de texto siempre visible en la parte inferior

## Estructura del Proyecto

```
chatbot/
├── backend/
│   ├── .venv/                    # Entorno virtual de Python
│   ├── main.py                   # API de FastAPI con perfiles y contexto
│   ├── database.py               # Modelos y funciones de SQLite
│   ├── migrate_db.py             # Script de migración de base de datos
│   ├── chatbot.db                # Base de datos SQLite (se crea automáticamente)
│   └── requirements.txt          # Dependencias de Python
├── frontend/
│   ├── index.html                # Interfaz con selector de perfiles
│   ├── styles.css                # Estilos modernos con tema oscuro
│   └── app.js                    # Lógica con gestión de perfiles y contexto
├── test_ollama_context.py        # Script de prueba básica de contexto
├── test_context_with_db.py       # Script de prueba completa con base de datos
├── test_full_system.py           # Test completo del sistema
├── README.md                     # Este archivo
├── UPGRADE_GUIDE.md              # Guía de actualización
├── CAMBIOS_IMPLEMENTADOS.md      # Documentación técnica de cambios
├── INDICADORES_VISUALES.md       # Documentación de indicadores de UI
└── MEJORAS_UI.md                 # Resumen de mejoras de interfaz
```

## Arquitectura

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

## 🤖 Sistema de Perfiles de Copiloto

### Perfiles Disponibles

El sistema incluye 5 perfiles predefinidos, cada uno con un `system_prompt` especializado:

| Perfil | ID | Icono | Descripción |
|--------|-----|-------|-------------|
| **Asistente genérico** | `generico` | 🤖 | Asistente académico universitario general |
| **Copiloto docente** | `docente` | 👨‍🏫 | Especializado en diseño instruccional y pedagogía |
| **Copiloto de robótica** | `robotica` | 🤖 | Experto en robótica móvil, sensores y actuadores |
| **Copiloto de programación** | `programacion` | 💻 | Especializado en Python, debugging y buenas prácticas |
| **Copiloto de investigación** | `investigacion` | 📚 | Metodología de investigación y escritura académica |

### Características de los Perfiles

Cada perfil incluye:
- ✅ **Identidad clara**: Define qué es el copiloto
- ✅ **Audiencia específica**: Para quién está diseñado
- ✅ **Reglas y límites**: Qué debe/no debe hacer
- ✅ **Formato de respuesta**: Cómo debe estructurar sus respuestas
- ✅ **Manejo de incertidumbre**: Admite cuando no sabe algo
- ✅ **Prevención de alucinaciones**: No inventa datos ni referencias

### System Prompt Editable

Los usuarios pueden:
1. Seleccionar un perfil predefinido
2. Cargar su plantilla con un click
3. Editar el `system_prompt` manualmente
4. Experimentar con diferentes configuraciones

El backend prioriza el `system_prompt` personalizado sobre el predefinido.

### Ejemplo: Perfil de Robótica

```
Eres un copiloto de robótica móvil educativa...

Reglas de seguridad críticas:
- SIEMPRE que la pregunta involucre conexiones eléctricas, 
  debes pedir datos faltantes ANTES de dar instrucciones
- Advierte sobre riesgos eléctricos...

Limitaciones:
- Si no conoces las especificaciones exactas, dilo explícitamente
- No asumas configuraciones por defecto sin confirmar
```

## Base de Datos SQLite

### Tablas

**conversations**
- `id`: ID único de la conversación
- `title`: Título de la conversación (generado del primer mensaje)
- `copilot_profile`: Perfil usado (generico, docente, robotica, etc.)
- `model`: Modelo LLM usado (llama3.2:3b, etc.)
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

**messages**
- `id`: ID único del mensaje
- `conversation_id`: FK a conversations
- `role`: 'system', 'user', o 'assistant'
- `content`: Contenido del mensaje
- `created_at`: Fecha de creación

## API Endpoints

### Chat
- **POST /chat**: Enviar mensaje al chatbot
  ```json
  {
    "message": "Explícame qué es la odometría diferencial",
    "conversation_id": 1,           // null para nueva conversación
    "model": "llama3.2:3b",
    "copilot_profile": "robotica",  // ID del perfil
    "system_prompt": "",            // Opcional: sobreescribe el del perfil
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 800,
    "num_ctx": 4096,
    "repeat_penalty": 1.1
  }
  ```

  **Respuesta:**
  ```json
  {
    "conversation_id": 1,
    "model": "llama3.2:3b",
    "copilot_profile": "robotica",
    "copilot_label": "Copiloto de robótica móvil",
    "system_prompt_used": "Eres un copiloto de robótica...",
    "reply": "La odometría diferencial es...",
    "metrics": {
      "wall_time_s": 3.566,
      "total_tokens": 294,
      "tokens_per_second": 42.94,
      ...
    }
  }
  ```

### Perfiles
- **GET /profiles**: Obtener todos los perfiles disponibles
  ```json
  {
    "generico": {
      "label": "Asistente genérico",
      "system_prompt": "Eres un asistente académico..."
    },
    "robotica": {
      "label": "Copiloto de robótica móvil",
      "system_prompt": "Eres un copiloto de robótica..."
    },
    ...
  }
  ```

### Gestión de Conversaciones
- **GET /conversations**: Listar todas las conversaciones (incluye perfil y modelo)
- **GET /conversations/{id}**: Obtener conversación específica con mensajes
- **POST /conversations**: Crear nueva conversación
  ```json
  {
    "title": "Conversación sobre robótica",
    "copilot_profile": "robotica",
    "model": "llama3.2:3b"
  }
  ```
- **DELETE /conversations/{id}**: Eliminar conversación

### Utilidad
- **GET /health**: Verificar estado del servidor
- **GET /**: Información general de la API
- **GET /docs**: Documentación interactiva (Swagger)

## Instalación y Uso

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
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Instalar dependencias (incluye SQLAlchemy)
pip install -r requirements.txt

# Ejecutar servidor (creará chatbot.db automáticamente)
uvicorn main:app --reload --port 8000
```

El backend estará disponible en:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 3. Configurar Frontend

```bash
cd frontend

# Iniciar servidor HTTP simple
python3 -m http.server 5500
```

El frontend estará disponible en:
- http://localhost:5500

### 4. Migrar Base de Datos (Si ya tienes datos)

Si ya tenías una base de datos de la versión anterior, ejecuta la migración:

```bash
cd backend
python3 migrate_db.py
```

Esto agregará las columnas `copilot_profile` y `model` sin perder datos.

### 5. Probar el Contexto con Base de Datos

```bash
# Desde la raíz del proyecto
cd backend
source .venv/bin/activate
python ../test_context_with_db.py
```

Este script demuestra que:
- El modelo recuerda información previa dentro de la misma conversación
- Nuevas conversaciones empiezan con contexto fresco
- Todo se guarda en SQLite

## Cómo Funciona el Contexto

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
// Modelo responde: "Te llamas Adrián"
```

## 🎨 Interfaz de Usuario

### Layout Principal

```
┌─────────────┬──────────────────────────────────────┐
│  Sidebar    │  [🤖 Conversando con: Perfil]        │
│             │                                       │
│  Nueva      │  ┌─────────────────────────┐        │
│  Chats      │  │  Mensaje Usuario        │        │
│  Config     │  └─────────────────────────┘        │
│             │                                       │
│  Recientes  │  ┌─────────────────────────┐        │
│             │  │  Respuesta Asistente    │  ← Scroll
│             │  └─────────────────────────┘        │
│             │                                       │
│             │  ══════════════════════════════      │
│             │  [Textarea] [Enviar]    ← Fijo aquí │
└─────────────┴──────────────────────────────────────┘
                                         [📊] ← Métricas
```

### Indicadores Visuales de Perfil

El sistema muestra **3 indicadores** del perfil activo:

1. **Badge en Panel de Configuración**
   - Ubicación: Panel derecho (arriba)
   - Diseño: Badge naranja con gradiente y animación de pulso
   - Muestra: Icono del perfil + "Perfil Activo" + Nombre

2. **Barra de Estado Superior**
   - Ubicación: Parte superior del chat (sticky)
   - Muestra: "🤖 Conversando con: [Nombre del Perfil]"
   - Se oculta en pantalla de bienvenida

3. **Nombre en Mensajes**
   - Cada respuesta muestra el nombre completo del perfil
   - Ejemplo: "COPILOTO DE ROBÓTICA MÓVIL"

### Funcionalidades de la Interfaz

#### Gestión de Perfiles
- **Selector de perfil**: Dropdown con 5 perfiles disponibles
- **Botón "Cargar plantilla"**: Carga el `system_prompt` del perfil seleccionado
- **Campo editable**: Textarea grande para modificar el `system_prompt`
- **Indicadores visuales**: Siempre sabes qué perfil está activo

#### Gestión de Contexto
- El frontend guarda automáticamente el `conversation_id` en `localStorage`
- Al recargar la página, se restaura la conversación anterior
- El botón "Limpiar conversación" inicia una nueva conversación
- Cada conversación guarda el perfil y modelo usado

#### Métricas en Modal
- **Botón flotante** 📊 en la esquina inferior derecha
- Click para abrir modal con métricas detalladas
- Cerrar con: X, click fuera, o tecla Escape
- No bloquea el chat (se muestra solo cuando se necesita)

#### Envío de Mensajes
- **Enter**: Envía el mensaje
- **Shift + Enter**: Nueva línea
- **Botón "Enviar"**: Click para enviar
- **Textarea autoexpandible**: Crece hasta 200px

#### Formulario Fijo
- La caja de texto está **fija en la parte inferior**
- Siempre visible, sin importar el scroll del chat
- El chat tiene padding inferior para no quedar tapado

### Parámetros Configurables

| Parámetro | Rango | Efecto |
|-----------|-------|--------|
| `model` | llama3.2:3b, etc. | Modelo LLM a usar |
| `temperature` | 0.0 - 1.2 | Mayor valor = más creatividad |
| `top_p` | 0.1 - 1.0 | Diversidad de palabras |
| `num_predict` | 20 - 1000 | Límite de tokens de respuesta |
| `num_ctx` | 2048/4096/8192 | Ventana de contexto |
| `repeat_penalty` | 1.0 - 2.0 | Penalización por repetición |

## 📊 Métricas Mostradas

Disponibles en el modal (botón flotante 📊):

| Métrica | Descripción |
|---------|-------------|
| **Perfil usado** | Nombre completo del perfil de copiloto utilizado |
| **Modelo** | Modelo LLM usado (ej: llama3.2:3b) |
| **Tiempo backend** | Tiempo total medido por Python |
| **Tiempo Ollama** | Tiempo reportado por el motor |
| **Carga modelo** | Tiempo de carga en memoria |
| **Tokens entrada** | Tokens del prompt (incluye historial + system_prompt) |
| **Tokens salida** | Tokens generados en la respuesta |
| **Tokens totales** | Suma de entrada + salida |
| **Generación** | Tiempo de generación de tokens |
| **Tokens/s** | Velocidad de generación |

**Ejemplo de métricas:**
```
Perfil usado: Copiloto de programación Python
Modelo: llama3.2:3b
Tokens entrada: 165
Tokens salida: 129
Tokens totales: 294
Tokens/s: 42.94
```

## 🧪 Pruebas del Sistema

### Test 1: Contexto y Memoria
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

### Test 3: Comparación de Perfiles

**Prompt de prueba:**
```
Explícame qué es la odometría diferencial y dame un ejemplo 
para estudiantes de primer semestre.
```

**Con "Asistente genérico":**
```
Respuesta general sobre odometría, explicación básica sin 
contexto específico de robótica.
```

**Con "Copiloto de robótica móvil":**
```
✅ Explicación técnica con ejemplos prácticos
✅ Mención de sensores (encoders)
✅ Advertencias sobre conexiones eléctricas
✅ Ejemplos con robots específicos
✅ Nivel adecuado para estudiantes de primer semestre
```

### Test 4: System Prompt Personalizado

1. Selecciona perfil "Programación"
2. Edita el system_prompt agregando: "Responde siempre en formato de lista numerada"
3. Envía: "¿Cómo debuggear un error en Python?"
4. Verifica que la respuesta esté en formato de lista numerada

### Test 5: Persistencia de Perfil

1. Selecciona perfil "Investigación"
2. Envía un mensaje
3. Recarga la página
4. Verifica en las métricas que el perfil se mantuvo

## Comandos Útiles

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

## Tecnologías Utilizadas

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

## Dependencias (requirements.txt)

```
aiosqlite==0.22.1
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.13.0
certifi==2026.5.20
charset-normalizer==3.4.7
click==8.4.1
fastapi==0.136.3
h11==0.16.0
idna==3.18
pydantic==2.13.4
pydantic-core==2.46.4
requests==2.34.2
sqlalchemy==2.0.50
starlette==1.2.1
typing-extensions==4.15.0
typing-inspection==0.4.2
urllib3==2.7.0
uvicorn==0.49.0
```

## 🎓 Uso Académico

### Comparación Genérico vs Especializado

Este proyecto es ideal para estudiar ingeniería de prompting y comparar:

| Aspecto | Asistente Genérico | Copiloto Especializado |
|---------|-------------------|------------------------|
| Claridad | General | Específica del dominio |
| Ejemplos | Abstractos | Prácticos y concretos |
| Advertencias | Genéricas | Específicas (ej: seguridad eléctrica) |
| Formato | Libre | Estructurado según perfil |
| Profundidad | Superficial | Ajustada a audiencia |

### Tabla de Evaluación

| Perfil | Prompt | ¿Cumple rol? | ¿Cumple formato? | ¿Alucina? | Tokens | Latencia |
|--------|--------|--------------|------------------|-----------|---------|----------|
| Genérico | "Explica X" | ✓/✗ | ✓/✗ | ✓/✗ | 234 | 1.2s |
| Robótica | "Explica X" | ✓/✗ | ✓/✗ | ✓/✗ | 345 | 1.8s |
| Docente | "Diseña clase de X" | ✓/✗ | ✓/✗ | ✓/✗ | 456 | 2.1s |

### Preguntas de Reflexión

1. ¿Qué perfil fue más útil y por qué?
2. ¿Observaste diferencias en claridad entre perfiles?
3. ¿El modelo inventó información en algún caso?
4. ¿Qué system prompt agregarías para tu proyecto?
5. ¿Cómo mejorarías los guardrails del sistema?

## Próximos Pasos (Opcional)

Para extender el proyecto:
- [x] ~~Agregar selector de conversaciones en la UI~~
- [x] ~~Sistema de perfiles de copiloto~~
- [x] ~~System prompts editables~~
- [x] ~~Indicadores visuales de perfil activo~~
- [ ] Implementar búsqueda en conversaciones
- [ ] Exportar conversaciones a PDF/TXT
- [ ] Agregar autenticación de usuarios
- [ ] Implementar RAG (Retrieval Augmented Generation)
- [ ] Agregar soporte para imágenes
- [ ] Integrar con sensores o robots físicos
- [ ] Crear más perfiles especializados (IA, Ciberseguridad, Medicina, etc.)

## Solución de Problemas

### El modelo no recuerda
✅ Verificar que estás enviando el `conversation_id` correcto
✅ Revisar en /docs que el historial se envía a Ollama
✅ Verificar que la base de datos se está creando (debe existir chatbot.db)

### Los perfiles no aparecen
✅ Hacer hard refresh del navegador (Cmd+Shift+R / Ctrl+Shift+R)
✅ Verificar que el backend esté corriendo
✅ Abrir http://localhost:8000/profiles y verificar que devuelve JSON

### Error: "no such column: copilot_profile"
✅ Ejecutar el script de migración: `python3 migrate_db.py`
✅ O eliminar la base de datos: `rm chatbot.db` (se recreará automáticamente)

### Los indicadores de perfil no se actualizan
✅ Hard refresh del navegador
✅ Verificar en la consola del navegador (F12) si hay errores
✅ Verificar que el backend devuelve `copilot_profile` y `copilot_label` en la respuesta

### Error de conexión a Ollama
✅ Verificar que Ollama está ejecutándose: `ollama list`
✅ Verificar que el modelo está descargado: `ollama pull llama3.2:3b`

### La conversación no se restaura al recargar
✅ Verificar que el navegador permite localStorage
✅ Abrir DevTools → Application → Local Storage → verificar `currentConversationId`

### El chat se desborda o la caja de texto desaparece
✅ Hard refresh del navegador
✅ Verificar que tienes los últimos archivos CSS y JS
✅ La caja de texto debe estar fija en la parte inferior

## Estado del Proyecto

✅ **Completado v3.0 - Sistema de Perfiles de Copiloto**:

### Backend
- ✅ Backend FastAPI con SQLite
- ✅ Sistema de perfiles de copiloto (5 perfiles predefinidos)
- ✅ Endpoint /profiles para gestión de perfiles
- ✅ System prompts editables y configurables
- ✅ Base de datos con columnas de perfil y modelo
- ✅ Script de migración para bases de datos existentes
- ✅ Validación de perfiles y parámetros
- ✅ API REST completa para CRUD de conversaciones

### Frontend
- ✅ Interfaz moderna con tema oscuro
- ✅ Selector de perfiles con carga de plantillas
- ✅ System prompt editable en tiempo real
- ✅ 3 indicadores visuales del perfil activo
- ✅ Métricas en modal (no bloquean el chat)
- ✅ Envío con Enter (Shift+Enter para nueva línea)
- ✅ Formulario fijo siempre visible
- ✅ Animaciones suaves y profesionales
- ✅ Responsive design

### Funcionalidades
- ✅ Contexto conversacional funcional
- ✅ Persistencia de perfil por conversación
- ✅ Tests de contexto exitosos
- ✅ Comparación genérico vs especializado
- ✅ Documentación completa actualizada

**Demostraciones:**
```
Contexto: Me llamo Adrián → ¿Cómo me llamo? → "Te llamas Adrián" ✅

Perfiles: "Explica odometría" 
  → Genérico: explicación básica
  → Robótica: explicación técnica con ejemplos prácticos ✅
```

## Licencia

Este proyecto es para uso académico y educativo.
