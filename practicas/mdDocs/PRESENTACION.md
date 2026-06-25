# 🎤 Presentación: Chatbot LLM con Perfiles de Copiloto

---

## 📌 Slide 1: Título

# Chatbot LLM Local con Sistema de Perfiles de Copiloto Especializado

**Práctica 3 - Ingeniería de Prompting**

Adrián Bazaldúa  
Junio 2026

---

## 📌 Slide 2: Problema

### ❌ Chatbots Genéricos

```
Usuario: "Explícame qué es la odometría diferencial"

Chatbot Genérico:
"La odometría diferencial es un método matemático..."
```

**Problemas:**
- Respuestas demasiado generales
- Sin contexto específico del dominio
- No adapta tono ni profundidad
- Sin advertencias de seguridad

---

## 📌 Slide 3: Solución

### ✅ Sistema de Perfiles Especializados

```
Usuario: "Explícame qué es la odometría diferencial"

Copiloto de Robótica:
"La odometría diferencial es fundamental en robots móviles.
Te explico con un ejemplo práctico usando dos ruedas...

⚠️ Advertencia: Al conectar los encoders, verifica el voltaje..."
```

**Ventajas:**
- ✅ Respuestas especializadas
- ✅ Ejemplos prácticos
- ✅ Advertencias relevantes
- ✅ Formato estructurado

---

## 📌 Slide 4: Arquitectura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Frontend   │─────→│   Backend    │─────→│   Ollama    │
│             │      │   FastAPI    │      │   llama3.2  │
│ - Selector  │←─────│              │←─────│             │
│ - Editor    │      │ - Perfiles   │      └─────────────┘
│ - Métricas  │      │ - Contexto   │
└─────────────┘      │ - SQLite     │
                     └──────────────┘
```

---

## 📌 Slide 5: Perfiles Implementados

| Perfil | Icono | Especialidad | Use Case |
|--------|-------|--------------|----------|
| **Genérico** | 🤖 | Académico general | Consultas generales |
| **Docente** | 👨‍🏫 | Diseño instruccional | Crear actividades |
| **Robótica** | 🤖 | Robótica móvil | Proyectos de robots |
| **Programación** | 💻 | Python | Debugging y código |
| **Investigación** | 📚 | Metodología | Papers y tesis |

---

## 📌 Slide 6: System Prompt - Ejemplo

### Copiloto de Robótica Móvil

```
Eres un copiloto de robótica móvil educativa.

Audiencia: Estudiantes universitarios de ingeniería

Reglas de seguridad críticas:
- SIEMPRE pedir datos faltantes antes de dar instrucciones
  (voltaje, corriente, modelo de componente)
- Advertir sobre riesgos eléctricos

Limitaciones:
- Si no conoces especificaciones, dilo explícitamente
- No asumas configuraciones por defecto
- No inventes datasheets
```

---

## 📌 Slide 7: Interfaz de Usuario

### Indicadores Visuales (3 tipos)

```
┌────────────────────────────────────────┐
│ Panel Config  │ 🤖 Conversando con:   │
│               │ Copiloto de Robótica  │
│ ┌───────────┐ │                       │
│ │ 🤖 Activo │ │ [Mensajes del chat]  │
│ │ Robótica  │ │                       │
│ └───────────┘ │                       │
│               │ ──────────────────────│
│ [System      │ [Textarea] [Enviar]   │
│  Prompt]     │                    📊 │
└────────────────────────────────────────┘
```

---

## 📌 Slide 8: Features Destacados

### 1. Métricas en Modal
- Botón flotante 📊
- No bloquea el chat
- Cierra con ESC o click fuera

### 2. System Prompt Editable
- Carga plantilla predefinida
- Edita en tiempo real
- Experimenta sin reiniciar

### 3. Formulario Fijo
- Siempre visible
- Enter para enviar
- Shift+Enter para nueva línea

---

## 📌 Slide 9: Demostración Práctica

### Test de Comparación

**Prompt:** "Explica la odometría diferencial para estudiantes de 1er semestre"

| Perfil | Claridad | Ejemplos | Advertencias | Tokens | Tiempo |
|--------|----------|----------|--------------|--------|--------|
| Genérico | ⭐⭐⭐ | Abstractos | ❌ | 234 | 1.2s |
| Robótica | ⭐⭐⭐⭐⭐ | Prácticos | ✅ | 345 | 1.8s |

**Diferencia observable** en claridad y utilidad ✅

---

## 📌 Slide 10: Contexto Conversacional

### Persistencia con SQLite

```
Usuario: "Me llamo Adrián y estudio robótica"
Bot: "¡Hola Adrián! ¿En qué puedo ayudarte con robótica?"

Usuario: "¿Qué estudio?"
Bot: "Estudias robótica"  ✅ RECUERDA

[Nueva conversación]
Usuario: "¿Qué estudio?"
Bot: "No tengo esa información"  ✅ CONTEXTO FRESCO
```

---

## 📌 Slide 11: Base de Datos

```sql
conversations
├── id: INTEGER
├── title: VARCHAR
├── copilot_profile: VARCHAR  ← Guarda perfil usado
├── model: VARCHAR            ← Guarda modelo usado
├── created_at: DATETIME
└── updated_at: DATETIME

messages
├── id: INTEGER
├── conversation_id: INTEGER (FK)
├── role: VARCHAR (system/user/assistant)
├── content: TEXT
└── created_at: DATETIME
```

---

## 📌 Slide 12: API REST

```
GET    /profiles              → Lista perfiles disponibles
POST   /chat                  → Envía mensaje con perfil
GET    /conversations         → Lista conversaciones
GET    /conversations/{id}    → Obtiene conversación
POST   /conversations         → Crea conversación
DELETE /conversations/{id}    → Elimina conversación
```

**Documentación automática:** `/docs` (Swagger)

---

## 📌 Slide 13: Tecnologías

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos embebida
- **Pydantic** - Validación de datos

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript ES6+** - Lógica y fetch API
- **localStorage** - Persistencia de sesión

### LLM
- **Ollama** - Motor de inferencia local
- **llama3.2:3b** - Modelo de lenguaje (3B parámetros)

---

## 📌 Slide 14: Estadísticas

### Líneas de Código
```
Backend:  ~450 líneas
Frontend: ~780 líneas
Tests:    ~200 líneas
Total:   ~1,430 líneas
```

### Características
```
Perfiles:     5
Endpoints:    8
Indicadores:  3
Métricas:    10
```

---

## 📌 Slide 15: Ingeniería de Prompting

### Elementos del System Prompt

```
1. Identidad      → "Eres un copiloto de..."
2. Audiencia      → "Para estudiantes de..."
3. Dominio        → "Especializado en..."
4. Reglas         → "Debes/No debes..."
5. Formato        → "Responde con..."
6. Límites        → "Si no sabes, di..."
7. Seguridad      → "Advierte sobre..."
```

---

## 📌 Slide 16: Guardrails

### Prevención de Alucinaciones

```python
Reglas en System Prompt:
✅ "No inventes referencias, autores ni DOI"
✅ "Si no tienes fuente verificable, dilo explícitamente"
✅ "Pide datos faltantes antes de asumir"
✅ "Separa hechos, inferencias y recomendaciones"
```

### Validación Backend
```python
✅ Validación de perfiles válidos
✅ Límites de longitud en prompts
✅ Límites de tokens de salida
✅ Timeout en llamadas a Ollama
```

---

## 📌 Slide 17: Casos de Uso

### 1. Educación
- Profesor diseña actividades
- Estudiante aprende conceptos
- Ajustado al nivel académico

### 2. Desarrollo
- Debugging de código
- Buenas prácticas
- Explicaciones paso a paso

### 3. Investigación
- Metodología académica
- Estructuración de papers
- Detección de vacíos conceptuales

---

## 📌 Slide 18: Resultados

### ✅ Objetivos Logrados

1. ✅ Sistema de perfiles especializado funcional
2. ✅ System prompts editables en tiempo real
3. ✅ Contexto conversacional persistente
4. ✅ Interfaz profesional con indicadores claros
5. ✅ API REST completa y documentada
6. ✅ Métricas detalladas capturadas
7. ✅ Base de datos con historial completo

---

## 📌 Slide 19: Comparación

### Antes vs Después

| Aspecto | Sin Perfiles | Con Perfiles |
|---------|-------------|--------------|
| Especialización | ❌ | ✅ |
| Formato | Libre | Estructurado |
| Advertencias | Genéricas | Específicas |
| Ejemplos | Abstractos | Prácticos |
| System Prompt | Fijo | Editable |
| Indicadores | ❌ | 3 tipos |

---

## 📌 Slide 20: Aprendizajes

### Conceptos Aplicados

1. **Ingeniería de Prompting**
   - Role prompting
   - Few-shot learning
   - Structured prompts

2. **Arquitectura Web**
   - API REST design
   - Cliente-servidor
   - Persistencia de datos

3. **UI/UX**
   - Indicadores visuales
   - Feedback inmediato
   - Modal vs inline

---

## 📌 Slide 21: Futuras Mejoras

### Próximos Pasos

- [ ] RAG (Retrieval Augmented Generation)
- [ ] Más perfiles (Medicina, Derecho, IA)
- [ ] Autenticación de usuarios
- [ ] Exportar conversaciones a PDF
- [ ] Búsqueda en conversaciones
- [ ] Soporte para imágenes
- [ ] Integración con sensores/robots

---

## 📌 Slide 22: Demostración en Vivo

### 🖥️ Demo Time

1. Selector de perfil
2. Carga de system prompt
3. Edición manual
4. Envío de mensaje
5. Indicadores visuales
6. Modal de métricas
7. Contexto conversacional

**URL:** http://localhost:5500

---

## 📌 Slide 23: Documentación

### Recursos Disponibles

```
📄 README.md                  - Documentación principal
📄 UPGRADE_GUIDE.md           - Guía de actualización
📄 CAMBIOS_IMPLEMENTADOS.md   - Changelog técnico
📄 INDICADORES_VISUALES.md    - Doc de indicadores
📄 MEJORAS_UI.md              - Doc de mejoras UI
📄 RESUMEN_PROYECTO.md        - Resumen ejecutivo
📄 PRESENTACION.md            - Esta presentación
```

---

## 📌 Slide 24: Conclusión

### 🎯 Logros del Proyecto

✅ **Sistema funcional y completo**
- Backend robusto con FastAPI
- Frontend moderno y responsive
- 5 perfiles especializados
- Documentación exhaustiva

✅ **Valor educativo**
- Demuestra ingeniería de prompting
- Compara genérico vs especializado
- Código bien estructurado

✅ **Extensible**
- Fácil agregar nuevos perfiles
- API REST bien diseñada
- Base de datos normalizada

---

## 📌 Slide 25: Preguntas

# ❓ ¿Preguntas?

**Contacto:**
- GitHub: [repositorio del proyecto]
- Email: [tu email]

**Demo disponible en:**
- http://localhost:5500 (Frontend)
- http://localhost:8000/docs (API Docs)

---

## 📌 Slide 26: Gracias

# 🙏 Gracias

**Proyecto:** Chatbot LLM con Perfiles de Copiloto  
**Versión:** 3.0  
**Estado:** ✅ Completado

**Tecnologías:**
FastAPI • SQLite • Ollama • llama3.2:3b • HTML/CSS/JS

**Estadísticas:**
~1,430 líneas • 5 perfiles • 8 endpoints • 17 archivos

---

# 🚀 ¡Gracias por su atención!
