# 📚 Guía Completa - Práctica 1

Guía paso a paso para completar y publicar la Práctica 1.

---

## 🎯 Objetivo de la Práctica

Explorar 6 modelos de lenguaje grande (LLMs) usando Ollama y documentar la experiencia en un reporte web profesional.

---

## 📋 Pasos para Completar

### Parte 1: Ejecutar la Práctica

#### 1. Instalar Ollama

```bash
# macOS
brew install ollama
brew services start ollama

# Verificar
ollama --version
```

**📸 Toma captura:** Guarda en `descargas/install-ollama.png`

#### 2. Descargar los 6 Modelos

```bash
ollama pull llama3.2:3b
ollama pull gemma2:2b
ollama pull qwen2.5:7b
ollama pull mistral:7b
ollama pull phi4
ollama pull tinyllama
```

**📸 Toma capturas:** Guarda cada una en `descargas/` con nombres:
- `01-llama32-3b.png`
- `02-gemma2-2b.png`
- `03-qwen25-7b.png`
- `04-mistral-7b.png`
- `05-phi4.png`
- `06-tinyllama.png`

#### 3. Verificar Modelos Instalados

```bash
ollama list
```

**📸 Toma captura:** Guarda en `descargas/ollama-list.png`

#### 4. Ejecutar Todos los Modelos

**Opción A: Automático (Recomendado)**

```bash
cd practicas/practica-1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python scripts/ejecutar_modelos.py
```

**Opción B: Manual**

Usa el mismo prompt para todos:
```
¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?
```

Ejecuta cada modelo:
```bash
ollama run llama3.2:3b "¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?"
ollama run gemma2:2b "¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?"
ollama run qwen2.5:7b "¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?"
ollama run mistral:7b "¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?"
ollama run phi4 "¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?"
ollama run tinyllama "¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?"
```

**📸 Toma capturas:** Guarda cada respuesta en `ejecuciones/` con nombres:
- `01-llama32-3b.png`
- `02-gemma2-2b.png`
- `03-qwen25-7b.png`
- `04-mistral-7b.png`
- `05-phi4.png`
- `06-tinyllama.png`

#### 5. Investigar en Hugging Face

Para cada modelo, visita su página en Hugging Face y toma nota:

| Modelo | URL de Hugging Face |
|--------|---------------------|
| Llama 3.2 | https://huggingface.co/meta-llama/Llama-3.2-3B |
| Gemma 2 | https://huggingface.co/google/gemma-2-2b |
| Qwen 2.5 | https://huggingface.co/Qwen/Qwen2.5-7B |
| Mistral | https://huggingface.co/mistralai/Mistral-7B-v0.1 |
| Phi-4 | https://huggingface.co/microsoft/phi-4 |
| TinyLlama | https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0 |

Documenta:
- Desarrollador
- Tipo de modelo
- Licencia
- Parámetros
- Lenguajes soportados
- Requisitos técnicos

---

### Parte 2: Completar el Reporte Web

#### 1. Navega a la Carpeta de Docs

```bash
cd practicas/practica-1/docs
```

#### 2. Completa Cada Sección

Edita los siguientes archivos y completa todas las secciones marcadas con `[Tu análisis]`, `[X minutos]`, etc.:

**✏️ `instalacion.md`**
- Agrega tus capturas de instalación
- Describe dificultades encontradas
- Califica la facilidad de instalación

**✏️ `modelos.md`**
- Agrega capturas de descargas
- Documenta tiempo de descarga de cada uno
- Agrega captura de `ollama list`

**✏️ `ejecuciones.md`**
- Agrega capturas de ejecuciones
- Copia las primeras líneas de cada respuesta
- Documenta tiempos de respuesta
- Evalúa calidad del español

**✏️ `comparativa.md`**
- Completa la tabla con info de Hugging Face
- Llena análisis comparativos
- Responde preguntas de análisis
- Da recomendaciones por caso de uso

**✏️ `reflexion.md`**
- Responde las 8 secciones de reflexión
- Da tu análisis personal
- Completa tablas de evaluación

**✏️ `conclusiones.md`**
- Resume tus hallazgos principales
- Documenta aprendizajes
- Propón trabajo futuro

#### 3. Actualiza Configuración

**✏️ `_config.yml`**

Verifica/actualiza:
```yaml
url: "https://adr1anbaz.github.io"  # Tu usuario
baseurl: "/prospectivaTecno"        # Tu repo
author: "Adrian Bazaldua"           # Tu nombre
```

#### 4. Prueba Localmente (Opcional)

```bash
# Instalar dependencias (solo primera vez)
bundle install

# Ejecutar Jekyll
bundle exec jekyll serve

# Abrir en navegador
open http://localhost:4000
```

---

### Parte 3: Publicar en GitHub Pages

#### 1. Commit y Push

```bash
cd ../../../  # Volver a la raíz del repo
git add .
git commit -m "Completar reporte de Práctica 1 con GitHub Pages"
git push
```

#### 2. Configurar GitHub Pages

1. Ve a tu repositorio en GitHub
2. **Settings** → **Pages**
3. Configura:
   - **Source:** Deploy from a branch
   - **Branch:** `main`
   - **Folder:** `/practicas/practica-1/docs`
4. **Save**

#### 3. Espera y Verifica

- Espera 2-5 minutos
- Visita: `https://adr1anbaz.github.io/prospectivaTecno/`
- Verifica que todo se vea bien
- Prueba la navegación
- Verifica que las imágenes carguen

---

## 📊 Checklist de Entregables

### Capturas de Pantalla

- [ ] Instalación de Ollama
- [ ] Descarga de Llama 3.2 3B
- [ ] Descarga de Gemma 2 2B
- [ ] Descarga de Qwen 2.5 7B
- [ ] Descarga de Mistral 7B
- [ ] Descarga de Phi-4
- [ ] Descarga de TinyLlama
- [ ] `ollama list` mostrando todos los modelos
- [ ] Ejecución de Llama 3.2 3B
- [ ] Ejecución de Gemma 2 2B
- [ ] Ejecución de Qwen 2.5 7B
- [ ] Ejecución de Mistral 7B
- [ ] Ejecución de Phi-4
- [ ] Ejecución de TinyLlama

### Documentación

- [ ] Instalación completada
- [ ] Modelos descargados documentados
- [ ] Ejecuciones documentadas
- [ ] Tabla comparativa completa
- [ ] Reflexión completa (8 secciones)
- [ ] Conclusiones completas

### Publicación

- [ ] Reporte web publicado en GitHub Pages
- [ ] URL accesible
- [ ] Navegación funcionando
- [ ] Imágenes cargando correctamente
- [ ] Sin errores 404

---

## 🎨 Tips para un Buen Reporte

### Capturas de Pantalla

✅ **Hacer:**
- Capturas limpias y legibles
- Mostrar información relevante
- Usar nombres descriptivos
- Formato PNG para mejor calidad

❌ **Evitar:**
- Capturas borrosas
- Demasiado contexto innecesario
- Espacios en nombres de archivo
- Formatos pesados

### Redacción

✅ **Hacer:**
- Ser específico y detallado
- Usar ejemplos concretos
- Justificar tus conclusiones
- Revisar ortografía

❌ **Evitar:**
- Respuestas genéricas
- Dejar secciones vacías
- Copiar/pegar sin análisis
- Ignorar preguntas

### Análisis

✅ **Hacer:**
- Comparar resultados
- Identificar patrones
- Proponer explicaciones
- Relacionar con teoría

❌ **Evitar:**
- Solo describir sin analizar
- Ignorar diferencias
- Conclusiones sin fundamento
- Análisis superficial

---

## 🆘 Solución de Problemas

### Ollama

**"Command not found"**
```bash
brew install ollama
brew services start ollama
```

**"Model not found"**
```bash
ollama pull nombre-del-modelo
```

**"Out of memory"**
- Cierra otras aplicaciones
- Prueba un modelo más pequeño primero
- Verifica requisitos de RAM

### GitHub Pages

**"Page build failed"**
- Revisa errores de sintaxis YAML
- Verifica frontmatter en archivos .md
- Mira el log de errores en GitHub Actions

**"Images not loading"**
- Verifica rutas relativas
- Usa nombres sin espacios
- Formato web (PNG, JPG)

**"Site not updating"**
- Espera 5 minutos
- Limpia caché (Cmd+Shift+R)
- Verifica configuración en Settings

---

## 📚 Recursos Útiles

### Documentación Oficial

- [Ollama Docs](https://ollama.com/docs)
- [Hugging Face](https://huggingface.co)
- [Just the Docs](https://just-the-docs.github.io/just-the-docs/)
- [Jekyll](https://jekyllrb.com/docs/)
- [GitHub Pages](https://docs.github.com/en/pages)

### Guías de Markdown

- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)

### Model Cards

- [Llama 3.2](https://huggingface.co/meta-llama/Llama-3.2-3B)
- [Gemma 2](https://huggingface.co/google/gemma-2-2b)
- [Qwen 2.5](https://huggingface.co/Qwen/Qwen2.5-7B)
- [Mistral](https://huggingface.co/mistralai/Mistral-7B-v0.1)
- [Phi-4](https://huggingface.co/microsoft/phi-4)
- [TinyLlama](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)

---

## ⏱️ Tiempo Estimado

| Actividad | Tiempo |
|:----------|:-------|
| Instalación de Ollama | 5-10 min |
| Descarga de 6 modelos | 30-60 min |
| Ejecuciones | 15-30 min |
| Investigación Hugging Face | 30-45 min |
| Completar reporte | 2-3 horas |
| Publicar en GitHub Pages | 10-15 min |
| **Total** | **4-5 horas** |

---

## ✅ Criterios de Evaluación

Asegúrate de cumplir con:

- ✅ Instalación documentada con capturas
- ✅ 6 modelos descargados y verificados
- ✅ Mismo prompt usado en todos los modelos
- ✅ Tabla comparativa completa con info de HF
- ✅ Reflexión personal detallada
- ✅ Análisis crítico y conclusiones
- ✅ Reporte web publicado y accesible
- ✅ Navegación funcionando correctamente
- ✅ Todas las imágenes cargando
- ✅ Redacción clara y profesional

---

## 🎉 ¡Listo!

Una vez completados todos los pasos, tendrás:

✨ Un reporte profesional publicado en web  
✨ Experiencia práctica con 6 LLMs diferentes  
✨ Conocimiento sobre licencias y modelos  
✨ Habilidades en GitHub Pages y Markdown  
✨ Análisis comparativo detallado  

**¡Éxito con tu práctica!** 🚀

---

**Autor:** Adrian Bazaldua  
**Última actualización:** 2026-06-01
