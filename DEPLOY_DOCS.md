# 🚀 Guía de Deployment - Documentación de Prácticas

## 📋 Resumen

El sistema de documentación ha sido reestructurado para tener:

- ✅ **Un solo sitio centralizado** en `/docs/`
- ✅ **Navegación por prácticas** en el menú lateral (no por secciones)
- ✅ **Cada práctica en una sola página** con toda su documentación
- ✅ **Deployment automático** mediante GitHub Actions

## 🏗️ Nueva Estructura

### Antes (Sistema Antiguo)
```
practicas/practica-1/docs/
├── index.md
├── instalacion.md
├── modelos.md
├── ejecuciones.md
├── comparativa.md
├── reflexion.md
└── conclusiones.md
```
**Problema**: Menú lateral mostraba secciones de UNA sola práctica.

### Ahora (Sistema Nuevo)
```
docs/
├── index.md          # Página principal
├── practica-1.md     # TODA la práctica 1 en una página
├── practica-2.md     # TODA la práctica 2 en una página
├── practica-3.md     # TODA la práctica 3 en una página
└── assets/           # Imágenes y recursos
```
**Ventaja**: Menú lateral navega entre prácticas completas.

## 🎯 Pasos para Activar GitHub Pages

### 1. Configurar GitHub Pages

Ve a: https://github.com/Adr1anBaz/prospectivaTecno/settings/pages

Configuración:
- **Source**: GitHub Actions
- **Branch**: (No aplica, usa Actions)

### 2. Verificar el Workflow

El workflow ya está actualizado en:
`.github/workflows/deploy-pages.yml`

Se ejecuta automáticamente cuando:
- Haces push a `main`
- Cambias archivos en `docs/**`

### 3. Activar Manualmente (Opcional)

Si necesitas forzar el deployment:

1. Ve a: https://github.com/Adr1anBaz/prospectivaTecno/actions
2. Selecciona "Deploy All Practices to GitHub Pages"
3. Click en "Run workflow"
4. Selecciona branch `main`
5. Click en "Run workflow"

### 4. Verificar el Deployment

Después de 2-3 minutos:

- **URL del sitio**: https://adr1anbaz.github.io/prospectivaTecno/
- **Estado del workflow**: https://github.com/Adr1anBaz/prospectivaTecno/actions

El workflow debe mostrar un ✅ verde.

## 📝 Hacer un Commit y Push

```bash
# Verificar cambios
git status

# Agregar todos los archivos nuevos
git add docs/ .github/workflows/deploy-pages.yml DEPLOY_DOCS.md

# Commit con mensaje descriptivo
git commit -m "Reestructurar documentación: sistema centralizado por prácticas

- Mover de practicas/practica-1/docs/ a docs/ centralizado
- Crear practica-1.md, practica-2.md, practica-3.md (páginas completas)
- Actualizar workflow para desplegar desde docs/
- Menú lateral ahora navega entre prácticas (no secciones)
- Cada práctica autocontenida en una sola página"

# Push a GitHub
git push origin main
```

## 🔍 Verificar Deployment

### 1. Verificar que el Workflow se Ejecutó

```bash
# Ver el estado del último workflow
gh run list --limit 1

# O visita:
# https://github.com/Adr1anBaz/prospectivaTecno/actions
```

### 2. Verificar el Sitio

Visita: https://adr1anbaz.github.io/prospectivaTecno/

Deberías ver:
- ✅ Página de inicio con índice de 3 prácticas
- ✅ Menú lateral con: Inicio, Práctica 1, Práctica 2, Práctica 3
- ✅ Cada práctica con toda su documentación en una sola página

### 3. Verificar la Navegación

- Click en "Práctica 1" → debe cargar toda la práctica
- Click en "Práctica 2" → debe cargar toda la práctica
- Click en "Práctica 3" → debe cargar toda la práctica
- Click en "Inicio" → debe regresar al índice

## 🐛 Troubleshooting

### El workflow falla

**Error común**: `bundle install` falla

**Solución**: Verifica que `docs/Gemfile` existe y contiene:
```ruby
source "https://rubygems.org"
gem "jekyll", "~> 4.3.0"
gem "just-the-docs", "0.8.2"
gem "jekyll-remote-theme"
gem "jekyll-seo-tag"
```

### El sitio no se ve bien

**Error común**: CSS no carga, links rotos

**Solución**: Verifica que `docs/_config.yml` tiene:
```yaml
baseurl: "/prospectivaTecno"
```

### Las imágenes no cargan

**Solución**: 
1. Verifica que las imágenes están en `docs/assets/practica-1/`
2. En los archivos `.md`, usa rutas relativas: `![Imagen](assets/practica-1/imagen.png)`

### El menú lateral no aparece

**Solución**: Cada archivo `.md` debe tener en el frontmatter:
```yaml
---
layout: default
title: Práctica N
nav_order: N
---
```

## ✅ Checklist de Deployment

Antes de hacer push, verifica:

- [ ] Todos los archivos `.md` tienen frontmatter correcto
- [ ] Las imágenes están en `docs/assets/`
- [ ] El `Gemfile` y `_config.yml` están en `docs/`
- [ ] El workflow apunta a `docs/` (no `practicas/practica-1/docs/`)
- [ ] Hiciste commit de todos los cambios
- [ ] Hiciste push a `main`

## 🎉 ¡Listo!

Una vez que el workflow termine (2-3 minutos), tu sitio estará disponible en:

**https://adr1anbaz.github.io/prospectivaTecno/**

Con navegación por prácticas en el menú lateral. 🚀

---

**Fecha**: Junio 2026  
**Autor**: Adrian Bazaldua
