# Práctica 1: Panorama de IA Generativa y LLM

Exploración práctica de modelos de lenguaje grande (LLMs) usando Ollama y Hugging Face.

## Objetivo

Explicar la diferencia entre IA, aprendizaje automático, IA generativa, embeddings, transformers y LLM, además de ganar experiencia práctica instalando y usando Ollama y consultando información en Hugging Face.

## Requisitos

- Python 3.9+
- Ollama instalado localmente
- Descargar y ejecutar mínimo 6 modelos LLM
- Comparar y documentar los modelos

## Modelos Sugeridos

| Modelo | Parámetros | Descripción |
|--------|------------|-------------|
| llama3.2:3b | 3B | Meta's Llama 3.2 |
| gemma2:2b | 2B | Google's Gemma 2 |
| qwen2.5:7b | 7B | Alibaba's Qwen 2.5 |
| mistral:7b | 7B | Mistral AI |
| phi4 | 14B | Microsoft Phi-4 |
| tinyllama | 1.1B | Tiny Llama |

## 📄 Reporte Web

El reporte de esta práctica está disponible como página web usando GitHub Pages:

🌐 **[Ver Reporte en Línea](https://adr1anbaz.github.io/prospectivaTecno/)** (una vez publicado)

La documentación completa incluye:
- ✅ Instalación de Ollama
- ✅ Descarga de modelos con capturas
- ✅ Ejecuciones comparativas
- ✅ Tabla comparativa detallada
- ✅ Reflexión personal
- ✅ Conclusiones

📂 [Ver código fuente del reporte](./docs/)

## Estructura de la Práctica

```
practica-1/
├── descargas/          # Capturas de descarga de modelos
├── ejecuciones/        # Capturas de ejecución con prompts
├── scripts/            # Scripts auxiliares
├── docs/               # Reporte web (Jekyll) de esta práctica
├── comparativa.md      # Tabla comparativa de modelos
├── reflexion.md        # Análisis y reflexión
├── GUIA_COMPLETA.md    # Guía extendida para completar la práctica
├── TODO_EQUIPO.md      # Pendientes del equipo
├── pyproject.toml      # Dependencias del entorno (scripts)
├── .gitignore
└── README.md           # Esta guía
```

> El entorno virtual (`.venv/`) no se versiona; créalo localmente cuando ejecutes scripts.

## Instalación

### 1. Instalar Ollama

**macOS:**
```bash
brew install ollama
brew services start ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Descargar desde [ollama.com](https://ollama.com/download)

### 2. Verificar Instalación

```bash
ollama --version
```

### 3. Crear Entorno Virtual (opcional para scripts)

```bash
cd practicas/practica-1
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install ollama huggingface-hub
```

## Pasos para Completar la Práctica

### Paso 1: Descargar Modelos

Descarga cada modelo y toma captura de pantalla:

```bash
ollama pull llama3.2:3b
ollama pull gemma2:2b
ollama pull qwen2.5:7b
ollama pull mistral:7b
ollama pull phi4
ollama pull tinyllama
```

**Guarda las capturas en:** `descargas/`

### Paso 2: Verificar Modelos Instalados

```bash
ollama list
```

Toma captura de pantalla mostrando todos los modelos instalados.

### Paso 3: Ejecutar Todos los Modelos con el Mismo Prompt

Usa el **mismo prompt** para todos los modelos y compara resultados.

**Prompt sugerido:**
```
¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?
```

**Ejemplo de ejecución:**
```bash
ollama run llama3.2:3b "¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?"
```

Repite para cada modelo y guarda capturas en `ejecuciones/`.

### Paso 4: Consultar Hugging Face

Para cada modelo, busca su tarjeta (model card) en [Hugging Face](https://huggingface.co/models) y documenta:

- 👨‍💻 Desarrollador
- 🏷️ Tipo de modelo (decoder-only, encoder-decoder, etc.)
- 📜 Licencia
- 🔢 Número de parámetros
- 🌐 Lenguajes soportados
- 💻 Requisitos técnicos (RAM, GPU, etc.)

### Paso 5: Crear Tabla Comparativa

Completa la tabla en `comparativa.md` (ver plantilla incluida).

### Paso 6: Reflexión

Responde las siguientes preguntas en `reflexion.md`:

1. **Facilidad de instalación:** ¿Qué tan fácil fue instalar y usar Ollama?
2. **Desempeño en español:** ¿Qué modelo(s) respondieron mejor en español?
3. **Diferencias de tamaño:** ¿Cómo afecta el tamaño del modelo a la velocidad y calidad?
4. **Importancia de licencias:** ¿Por qué es importante revisar la licencia de un modelo?
5. **LLMs en academia:** ¿Por qué los LLMs no deben ser la única fuente de información académica?
6. **Ejecución local:** ¿Qué ventajas y limitaciones tiene ejecutar modelos localmente vs. usar APIs?

## Plantillas Incluidas

- `comparativa.md` - Tabla para comparar modelos
- `reflexion.md` - Guía para análisis personal

## Entregables

1. ✅ Capturas de pantalla de descargas (6 modelos mínimo)
2. ✅ Capturas de ejecución con el mismo prompt (6 modelos)
3. ✅ Captura de `ollama list` mostrando todos los modelos
4. ✅ Tabla comparativa completa (comparativa.md)
5. ✅ Documento de reflexión (reflexion.md)

## Recursos Adicionales

- [Documentación de Ollama](https://ollama.com/docs)
- [Hugging Face Models](https://huggingface.co/models)
- [Página de la actividad](https://hubergiron.github.io/llm-ollama/)

## Comandos Útiles

```bash
# Ver todos los modelos instalados
ollama list

# Ejecutar modelo interactivamente
ollama run llama3.2:3b

# Ejecutar modelo con prompt único
ollama run llama3.2:3b "tu prompt aquí"

# Eliminar un modelo
ollama rm modelo:tag

# Ver información de un modelo
ollama show llama3.2:3b
```

## Notas

- Los modelos más grandes (7B+) requieren más RAM y tiempo de descarga
- La primera ejecución de cada modelo puede tardar más
- Usa el mismo prompt para hacer comparaciones justas
- Documenta cualquier observación interesante durante el proceso

---

**Autor:** Adrian Bazaldua  
**Curso:** IA Generativa y LLMs - Verano 2026
