# 📋 TO-DO Para el Equipo - Práctica 1

## ✅ Checklist de Tareas Pendientes

### 1. Ejecutar Ollama y Modelos

- [ ] Instalar Ollama
  ```bash
  brew install ollama
  brew services start ollama
  ```

- [ ] Descargar los 6 modelos (tomar capturas de cada uno):
  - [ ] `ollama pull llama3.2:3b` → guardar como `descargas/01-llama32-3b.png`
  - [ ] `ollama pull gemma2:2b` → guardar como `descargas/02-gemma2-2b.png`
  - [ ] `ollama pull qwen2.5:7b` → guardar como `descargas/03-qwen25-7b.png`
  - [ ] `ollama pull mistral:7b` → guardar como `descargas/04-mistral-7b.png`
  - [ ] `ollama pull phi4` → guardar como `descargas/05-phi4.png`
  - [ ] `ollama pull tinyllama` → guardar como `descargas/06-tinyllama.png`

- [ ] Verificar instalación:
  - [ ] `ollama list` → guardar como `descargas/ollama-list.png`

### 2. Ejecutar Modelos con el Mismo Prompt

**Prompt a usar para TODOS los modelos:**
```
¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?
```

Ejecutar cada modelo y tomar captura de la respuesta completa:

- [ ] `ollama run llama3.2:3b "..."` → `ejecuciones/01-llama32-3b.png`
- [ ] `ollama run gemma2:2b "..."` → `ejecuciones/02-gemma2-2b.png`
- [ ] `ollama run qwen2.5:7b "..."` → `ejecuciones/03-qwen25-7b.png`
- [ ] `ollama run mistral:7b "..."` → `ejecuciones/04-mistral-7b.png`
- [ ] `ollama run phi4 "..."` → `ejecuciones/05-phi4.png`
- [ ] `ollama run tinyllama "..."` → `ejecuciones/06-tinyllama.png`

**Importante:** Mide y anota el tiempo de respuesta de cada uno.

### 3. Investigar en Hugging Face

Para cada modelo, visita su página en Hugging Face y documenta:

- [ ] **Llama 3.2 3B:** https://huggingface.co/meta-llama/Llama-3.2-3B
  - Desarrollador: Meta
  - Licencia: Llama 3 Community License
  - Lenguajes: Multilingüe
  - Requisitos: _completar_

- [ ] **Gemma 2 2B:** https://huggingface.co/google/gemma-2-2b
  - Desarrollador: Google DeepMind
  - Licencia: Gemma License
  - Lenguajes: _completar_
  - Requisitos: _completar_

- [ ] **Qwen 2.5 7B:** https://huggingface.co/Qwen/Qwen2.5-7B
  - Desarrollador: Alibaba
  - Licencia: Apache 2.0
  - Lenguajes: _completar_
  - Requisitos: _completar_

- [ ] **Mistral 7B:** https://huggingface.co/mistralai/Mistral-7B-v0.1
  - Desarrollador: Mistral AI
  - Licencia: Apache 2.0
  - Lenguajes: _completar_
  - Requisitos: _completar_

- [ ] **Phi-4:** https://huggingface.co/microsoft/phi-4
  - Desarrollador: Microsoft
  - Licencia: MIT
  - Lenguajes: _completar_
  - Requisitos: _completar_

- [ ] **TinyLlama:** https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
  - Desarrollador: TinyLlama Team
  - Licencia: Apache 2.0
  - Lenguajes: _completar_
  - Requisitos: _completar_

### 4. Completar el Reporte Web

Los archivos están en `docs/`. Busca los comentarios `<!-- TODO: ... -->` y completa:

#### 📄 `docs/instalacion.md`
- [ ] Actualizar especificaciones del sistema (RAM, procesador)
- [ ] Completar sección "Dificultades Encontradas"
- [ ] Completar análisis de "Facilidad de Instalación"

#### 📄 `docs/modelos.md`
- [ ] Agregar tiempos de descarga reales
- [ ] Agregar observaciones de cada modelo
- [ ] Completar "Observaciones Generales"

#### 📄 `docs/ejecuciones.md`
- [ ] Copiar primeras líneas de cada respuesta
- [ ] Agregar tiempos de respuesta medidos
- [ ] Evaluar calidad del español de cada modelo
- [ ] Completar análisis comparativos
- [ ] Completar sección "Mejor Desempeño en Español"
- [ ] Completar "Relación Tamaño vs Calidad"

#### 📄 `docs/comparativa.md`
- [ ] Completar análisis "Mejor desempeño en español"
- [ ] Completar "Relación entre parámetros y calidad"
- [ ] Completar "Qué modelo fue más rápido"
- [ ] Dar recomendaciones para cada caso de uso:
  - Chatbot en español
  - Aplicación móvil
  - Investigación académica
  - Producción comercial

#### 📄 `docs/reflexion.md`
- [ ] Responder las 8 secciones de reflexión:
  1. Facilidad de Instalación
  2. Desempeño en Español
  3. Relación Tamaño vs. Calidad
  4. Importancia de las Licencias
  5. LLMs como Fuente Académica
  6. Ejecución Local vs. APIs
  7. Conceptos Clave Aprendidos
  8. Reflexión Final

#### 📄 `docs/conclusiones.md`
- [ ] Completar resumen ejecutivo
- [ ] Documentar aprendizajes principales
- [ ] Completar reflexión personal final
- [ ] Agregar agradecimientos

### 5. Publicar en GitHub Pages

- [ ] Hacer commit de todos los cambios:
  ```bash
  git add .
  git commit -m "Completar contenido del reporte de Práctica 1"
  git push
  ```

- [ ] Configurar GitHub Pages:
  1. Ir a Settings → Pages
  2. Source: Deploy from a branch
  3. Branch: `main`
  4. Folder: `/practicas/practica-1/docs`
  5. Save

- [ ] Verificar que el sitio cargue correctamente:
  - URL: https://adr1anbaz.github.io/prospectivaTecno/

### 6. Verificación Final

- [ ] Navegación funciona
- [ ] Todas las imágenes cargan
- [ ] No hay secciones con "_pendiente_"
- [ ] No hay comentarios `<!-- TODO -->` visibles
- [ ] Tablas completadas
- [ ] Análisis coherentes y completos

---

## 🔍 Dónde Buscar los TODOs

Usa este comando para encontrar todas las secciones pendientes:

```bash
cd practicas/practica-1/docs
grep -r "TODO" *.md
grep -r "_pendiente_" *.md
```

---

## 📞 Ayuda

Si tienen dudas, revisen:
- `GUIA_COMPLETA.md` - Guía paso a paso
- `README.md` - Instrucciones generales
- `docs/README_DOCS.md` - Instrucciones de publicación

---

## ⏱️ Tiempo Estimado

| Tarea | Tiempo |
|-------|--------|
| Descargar modelos | 30-60 min |
| Ejecutar y tomar capturas | 20-30 min |
| Investigar Hugging Face | 30-45 min |
| Completar reporte | 2-3 horas |
| Publicar | 10 min |
| **Total** | **3.5-5 horas** |

---

**¡Éxito con la práctica!** 🚀
