# Guía de Actualización: Sistema de Perfiles de Copiloto

Este documento explica cómo actualizar tu chatbot con el nuevo sistema de perfiles de copiloto especializado.

## 📋 Resumen de Cambios

### Backend
- ✅ Agregado diccionario `COPILOT_PROFILES` con 5 perfiles predefinidos
- ✅ Nuevo endpoint `/profiles` para obtener perfiles disponibles
- ✅ Campos adicionales en ChatRequest: `copilot_profile`, `system_prompt`
- ✅ Campos adicionales en ChatResponse: `copilot_profile`, `copilot_label`, `system_prompt_used`
- ✅ Base de datos actualizada con columnas `copilot_profile` y `model`

### Frontend
- ✅ Selector de perfil de copiloto
- ✅ Botón "Cargar plantilla del perfil"
- ✅ Campo editable de system_prompt
- ✅ Métricas actualizadas muestran perfil y modelo usado
- ✅ Mensajes del asistente muestran el label del copiloto

## 🚀 Pasos para Actualizar

### 1. Backend

#### Opción A: Si ya tienes una base de datos existente

```bash
cd backend
python migrate_db.py
```

Este script agregará las columnas `copilot_profile` y `model` a tu base de datos existente sin perder datos.

#### Opción B: Base de datos nueva

Si prefieres empezar de cero:

```bash
cd backend
rm chatbot.db  # Elimina la base de datos anterior
# La nueva base de datos se creará automáticamente al iniciar el servidor
```

### 2. Iniciar el Backend

```bash
cd backend
source .venv/bin/activate  # En macOS/Linux
# o
.venv\Scripts\activate  # En Windows

uvicorn main:app --reload --port 8000
```

Verifica que funcione:
- http://localhost:8000/docs
- http://localhost:8000/profiles

### 3. Iniciar el Frontend

```bash
cd frontend
python -m http.server 5500
```

Abre: http://localhost:5500

## 🎯 Características Nuevas

### 1. Perfiles de Copiloto Disponibles

- **Asistente genérico**: Para consultas generales académicas
- **Copiloto docente universitario**: Para diseño de clases y actividades
- **Copiloto de robótica móvil**: Para temas de robótica educativa
- **Copiloto de programación Python**: Para código y debugging
- **Copiloto de investigación académica**: Para papers y metodología

### 2. System Prompt Editable

Puedes:
- Seleccionar un perfil y cargar su plantilla
- Editar el system_prompt manualmente
- Experimentar con diferentes configuraciones

### 3. Métricas Mejoradas

Ahora puedes ver:
- Perfil de copiloto usado
- Modelo LLM usado
- Todas las métricas anteriores (tokens, latencia, etc.)

## 🧪 Pruebas Sugeridas

### Comparación Genérico vs Especializado

1. **Selecciona**: "Asistente genérico"
2. **Pregunta**: "Explícame qué es la odometría diferencial"
3. **Observa**: La respuesta

4. **Cambia a**: "Copiloto de robótica móvil"
5. **Pregunta**: Exactamente lo mismo
6. **Compara**: ¿Cuál respuesta es más útil?

### Prueba de System Prompt Personalizado

1. Selecciona cualquier perfil
2. Haz clic en "Cargar plantilla del perfil"
3. Edita el system_prompt agregando: "Responde siempre en formato de lista numerada"
4. Envía una pregunta
5. Observa cómo el formato cambia

## 📊 Estructura de Datos

### Conversación en Base de Datos

```python
{
  "id": 1,
  "title": "Nueva conversación",
  "copilot_profile": "robotica",
  "model": "llama3.2:3b",
  "created_at": "2026-06-10T...",
  "updated_at": "2026-06-10T...",
  "messages": [...]
}
```

### Respuesta de Chat

```json
{
  "conversation_id": 1,
  "model": "llama3.2:3b",
  "copilot_profile": "robotica",
  "copilot_label": "Copiloto de robótica móvil",
  "system_prompt_used": "Eres un copiloto de robótica...",
  "reply": "La odometría diferencial...",
  "metrics": {
    "wall_time_s": 2.341,
    "total_tokens": 450,
    ...
  }
}
```

## 🔧 Agregar Nuevos Perfiles

Edita `backend/main.py`:

```python
COPILOT_PROFILES: Dict[str, Dict[str, str]] = {
    # ... perfiles existentes ...
    
    "mi_perfil": {
        "label": "Mi Copiloto Personalizado",
        "system_prompt": (
            "Eres un copiloto especializado en [dominio]. "
            "Tus características principales son: [lista]. "
            "Debes [reglas y límites]."
        ),
    },
}
```

Luego actualiza `frontend/index.html`:

```html
<select id="copilot_profile">
  <!-- opciones existentes -->
  <option value="mi_perfil">Mi Copiloto Personalizado</option>
</select>
```

## 🎓 Para la Práctica

### Tabla de Pruebas

| Perfil | Prompt | ¿Cumple rol? | ¿Cumple formato? | ¿Alucina? | Tokens | Latencia |
|--------|--------|--------------|------------------|-----------|---------|----------|
| Genérico | ... | ✓/✗ | ✓/✗ | ✓/✗ | 234 | 1.2s |
| Robótica | ... | ✓/✗ | ✓/✗ | ✓/✗ | 345 | 1.8s |

### Preguntas de Reflexión

1. ¿Qué perfil fue más útil y por qué?
2. ¿Observaste diferencias en el formato de respuesta?
3. ¿El modelo inventó información en algún caso?
4. ¿Qué cambiarías en los system prompts?
5. ¿Cómo mejorarías los guardrails?

## 🐛 Troubleshooting

### Error: "Perfil no válido"

- Verifica que el perfil existe en `COPILOT_PROFILES`
- Verifica que el frontend usa el mismo ID

### No se cargan los perfiles

- Verifica que el backend esté corriendo
- Abre la consola del navegador (F12)
- Verifica que `http://localhost:8000/profiles` responda

### La base de datos no migró

```bash
cd backend
python migrate_db.py
```

Si falla, elimina `chatbot.db` y deja que se recree.

## 📚 Recursos

- [Instrucciones completas](./instructions.html)
- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Ollama API](https://docs.ollama.com/api/)

---

✅ **¡Listo!** Ahora tienes un chatbot con perfiles de copiloto especializados + historial persistente.
