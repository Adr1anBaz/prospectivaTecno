# 📚 Documentación de Prácticas - IA y Prospectiva Tecnológica

Este directorio contiene la documentación centralizada de todas las prácticas del curso, desplegada mediante GitHub Pages con Jekyll.

## 🏗️ Estructura

```
docs/
├── _config.yml          # Configuración de Jekyll
├── Gemfile             # Dependencias Ruby
├── index.md            # Página principal
├── practica-1.md       # Práctica 1 completa (una sola página)
├── practica-2.md       # Práctica 2 completa (una sola página)
├── practica-3.md       # Práctica 3 completa (una sola página)
└── assets/             # Recursos estáticos (imágenes, etc.)
    └── practica-1/     # Imágenes de la práctica 1
```

## 🎨 Sistema de Navegación

El menú lateral permite navegar entre prácticas:

- **Inicio**: Página principal con índice de prácticas
- **Práctica 1**: IA Generativa y LLM (toda la documentación en una página)
- **Práctica 2**: Benchmark de LLMs (toda la documentación en una página)
- **Práctica 3**: Chatbot con Contexto (toda la documentación en una página)

Cada práctica es **autocontenida** en una sola página con toda su documentación, eliminando la necesidad de navegar entre secciones.

## 🚀 Deployment

### Automático (GitHub Actions)

El sitio se despliega automáticamente cuando se hace push a `main` y hay cambios en:
- `docs/**`
- `.github/workflows/deploy-pages.yml`

### Local

Para probar localmente:

```bash
cd docs

# Instalar dependencias
bundle install

# Servir localmente
bundle exec jekyll serve

# Visitar http://localhost:4000/prospectivaTecno/
```

## 📝 Agregar Nueva Práctica

1. Crear archivo `practica-N.md` en `docs/`
2. Usar el siguiente frontmatter:

```markdown
---
layout: default
title: Práctica N
nav_order: N+1  # (index.md es 1, practica-1.md es 2, etc.)
description: "Breve descripción"
---

# Práctica N: Título
{: .fs-9 }

Subtítulo descriptivo
{: .fs-6 .fw-300 }

[Ver en GitHub](URL){: .btn .btn-primary }

---

## Contenido...
```

3. Actualizar `index.md` con el enlace a la nueva práctica
4. Hacer commit y push

## 🎨 Tema

Este sitio usa el tema [Just the Docs](https://just-the-docs.github.io/just-the-docs/), que ofrece:

- Búsqueda integrada
- Navegación responsive
- Código con syntax highlighting
- Tablas de contenido automáticas
- Modo claro/oscuro

## 📦 Dependencias

- Ruby 3.1+
- Jekyll 4.3+
- just-the-docs 0.8.2
- jekyll-remote-theme
- jekyll-seo-tag

## 🔗 URLs

- **Repositorio**: https://github.com/Adr1anBaz/prospectivaTecno
- **GitHub Pages**: https://adr1anbaz.github.io/prospectivaTecno/
- **Documentación Jekyll**: https://jekyllrb.com/docs/
- **Tema Just the Docs**: https://just-the-docs.github.io/just-the-docs/

## 📄 Licencia

Contenido académico para uso educativo.
