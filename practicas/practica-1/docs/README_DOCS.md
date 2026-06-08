# Documentación del Reporte - Práctica 1

Este directorio contiene el reporte de la Práctica 1 en formato web usando Jekyll y Just the Docs.

## Estructura

```
docs/
├── _config.yml           # Configuración de Jekyll
├── Gemfile              # Dependencias Ruby
├── index.md             # Página principal
├── instalacion.md       # Sección 1: Instalación
├── modelos.md           # Sección 2: Modelos descargados
├── ejecuciones.md       # Sección 3: Ejecuciones
├── comparativa.md       # Sección 4: Tabla comparativa
├── reflexion.md         # Sección 5: Reflexión
├── conclusiones.md      # Sección 6: Conclusiones
└── assets/
    └── img/             # Imágenes del sitio
```

## Publicar en GitHub Pages

### Opción 1: Desde GitHub (Recomendado)

1. **Haz push de los cambios:**
   ```bash
   git add .
   git commit -m "Agregar reporte de Práctica 1 con GitHub Pages"
   git push
   ```

2. **Configurar GitHub Pages:**
   - Ve a tu repositorio en GitHub
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/practicas/practica-1/docs`
   - Guarda los cambios

3. **Espera unos minutos** y tu sitio estará en:
   ```
   https://adr1anbaz.github.io/prospectivaTecno/
   ```

### Opción 2: Probar Localmente

Para probar el sitio antes de publicar:

1. **Instalar Ruby y Bundler:**
   ```bash
   # macOS (con Homebrew)
   brew install ruby
   gem install bundler
   
   # Linux
   sudo apt install ruby-full
   gem install bundler
   ```

2. **Instalar dependencias:**
   ```bash
   cd practicas/practica-1/docs
   bundle install
   ```

3. **Ejecutar Jekyll localmente:**
   ```bash
   bundle exec jekyll serve
   ```

4. **Ver el sitio:**
   Abre en tu navegador: `http://localhost:4000`

## Completar el Reporte

### 1. Agregar Capturas de Pantalla

Copia tus capturas a las carpetas correspondientes:

```bash
# Capturas de descargas
cp ~/Screenshots/ollama-*.png ../descargas/

# Capturas de ejecuciones
cp ~/Screenshots/run-*.png ../ejecuciones/
```

Las imágenes se referencian en los archivos .md con:
```markdown
![Descripción](../descargas/nombre-imagen.png)
```

### 2. Completar Contenido

Edita los archivos `.md` y completa las secciones marcadas con:
- `[Tu análisis]`
- `[X minutos]`
- `[Tu observación]`
- etc.

### 3. Personalizar Configuración

Edita `_config.yml` y actualiza:
```yaml
url: "https://adr1anbaz.github.io"  # Tu usuario de GitHub
baseurl: "/prospectivaTecno"         # Nombre de tu repo
author: "Adrian Bazaldua"            # Tu nombre
```

### 4. Agregar Logo (Opcional)

Si tienes un logo, agrégalo como:
```bash
cp tu-logo.png assets/img/logo.png
```

## Navegación del Sitio

La navegación se controla con el frontmatter en cada archivo:

```yaml
---
layout: default
title: Título de la Página
nav_order: 1           # Orden en el menú (1-7)
description: "..."
---
```

Orden actual:
1. Inicio
2. Instalación
3. Modelos Descargados
4. Ejecuciones
5. Tabla Comparativa
6. Reflexión
7. Conclusiones

## Características del Tema

### Bloques Especiales

```markdown
{: .note }
> Esto es una nota

{: .highlight }
Esto es un highlight

{: .warning }
Esto es una advertencia
```

### Tabla de Contenidos

Se genera automáticamente con:
```markdown
## Tabla de Contenidos
{: .no_toc .text-delta }

1. TOC
{:toc}
```

### Botones

```markdown
[Texto del Botón](./enlace){: .btn .btn-primary }
```

### Código

```markdown
```bash
comando aquí
\```
```

## Solución de Problemas

### "Page build failed"

- Revisa que no haya errores de sintaxis en los archivos .md
- Asegúrate de que el frontmatter YAML esté bien formado
- Verifica que las rutas de las imágenes sean correctas

### "Images not loading"

- Las rutas deben ser relativas: `../descargas/imagen.png`
- Los nombres de archivo no deben tener espacios (usa guiones)
- Las imágenes deben estar en formato web (PNG, JPG, GIF)

### "Site not updating"

- GitHub Pages puede tardar 1-5 minutos en actualizar
- Limpia caché del navegador (Cmd+Shift+R en Chrome/Firefox)
- Verifica en Settings → Pages que esté configurado correctamente

## Recursos

- [Just the Docs Documentation](https://just-the-docs.github.io/just-the-docs/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Markdown Guide](https://www.markdownguide.org/)

## Checklist de Publicación

- [ ] Capturas de pantalla agregadas en `descargas/` y `ejecuciones/`
- [ ] Todas las secciones completadas (sin `[Tu análisis]`)
- [ ] URLs en `_config.yml` actualizadas
- [ ] Archivos commiteados y pusheados
- [ ] GitHub Pages configurado en Settings
- [ ] Sitio accesible y funcionando
- [ ] Navegación probada
- [ ] Imágenes cargando correctamente

---

**¡Tu reporte como página web está listo!** 🎉
