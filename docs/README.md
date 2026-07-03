# Documentación de Prácticas — IA y Prospectiva Tecnológica

Este directorio contiene la documentación centralizada de todas las prácticas del curso, desplegada mediante GitHub Pages con Jekyll y el tema [just-the-docs](https://just-the-docs.github.io/just-the-docs/).

## Estructura

```
docs/
├── _config.yml          # Configuración de Jekyll
├── Gemfile              # Dependencias Ruby
├── index.md             # Página principal con el índice de prácticas
├── practica-1.md        # Práctica 1: Panorama de IA Generativa y LLM
├── practica-2.md        # Práctica 2: Selección de plataforma y benchmark
├── practica-3.md        # Práctica 3: Chatbot local con contexto (SQLite)
├── practica-4.md        # Práctica 4: Copilotos especializados
├── practica-5.md        # Práctica 5: Chatbot híbrido con APIs externas
├── practica-6.md        # Práctica 6: Arquitectura LLM + MQTT
├── assets/              # Datos crudos de baterías y gráficas por práctica
└── imgs/                # Capturas de pantalla por práctica (pr3, pr4, pr5, ...)
```

Cada práctica es **autocontenida** en una sola página con toda su documentación (objetivo, arquitectura, resultados y análisis).

## Navegación

El menú lateral permite moverse entre las páginas:

- **Inicio** (`index.md`): índice con la descripción de cada práctica.
- **Práctica 1**: Panorama de IA Generativa y LLM.
- **Práctica 2**: Selección de plataforma y benchmark de LLMs.
- **Práctica 3**: Chatbot LLM local con contexto (SQLite).
- **Práctica 4**: Copilotos especializados con Ollama.
- **Práctica 5**: Chatbot híbrido con Ollama y APIs externas.
- **Práctica 6**: Evaluación de arquitectura LLM + MQTT.

## Deployment

### Automático (GitHub Actions)

El sitio se despliega automáticamente al hacer push a `main` cuando hay cambios en:
- `docs/**`
- `.github/workflows/deploy-pages.yml`

### Local

```bash
cd docs
bundle install
bundle exec jekyll serve   # http://localhost:4000/prospectivaTecno/
```

## Agregar una nueva práctica

1. Crear `docs/practica-N.md` con el frontmatter:

```markdown
---
layout: default
title: Práctica N
nav_order: N+1   # index.md es 1, practica-1.md es 2, etc.
description: "Breve descripción"
---

# Práctica N: Título
{: .fs-9 }

Subtítulo descriptivo
{: .fs-6 .fw-300 }

[Ver en GitHub](URL){: .btn .btn-primary }
```

2. Añadir la descripción y el enlace en `index.md`.
3. Colocar datos/gráficas en `assets/practica-N/` y capturas en `imgs/prN/`.
4. Commit y push.

## Dependencias

- Ruby 3.1+, Jekyll 4.3+, just-the-docs 0.8.2, jekyll-remote-theme, jekyll-seo-tag.

## URLs

- **Repositorio**: https://github.com/Adr1anBaz/prospectivaTecno
- **GitHub Pages**: https://adr1anbaz.github.io/prospectivaTecno/

## Licencia

Contenido académico para uso educativo.
