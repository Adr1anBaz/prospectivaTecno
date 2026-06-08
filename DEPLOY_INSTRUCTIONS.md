# 📦 Instrucciones de Deploy - GitHub Pages

## ✅ Todo está listo para deployar

La presentación está completamente configurada y lista para subir a GitHub Pages.

## 🚀 Pasos para Deploy

### 1. Crear el Repositorio en GitHub

Ve a [github.com/new](https://github.com/new) y crea un nuevo repositorio:

- **Nombre del repositorio:** `presentacion-unitree-go2`
- **Visibilidad:** Público (necesario para GitHub Pages gratuito)
- **NO** inicialices con README, .gitignore o licencia (ya los tenemos)

### 2. Conectar y Subir el Código

En esta carpeta (`presentacion-proyecto`), ejecuta:

```bash
# Reemplaza 'TU_USUARIO' con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/presentacion-unitree-go2.git

# Subir el código
git push -u origin main
```

### 3. Activar GitHub Pages

1. Ve a tu repositorio en GitHub
2. Click en **Settings** (Configuración)
3. En el menú lateral, click en **Pages**
4. En **Source**, selecciona: **GitHub Actions**
5. ¡Listo! El workflow se ejecutará automáticamente

### 4. Esperar el Deploy (1-2 minutos)

- Ve a la pestaña **Actions** en tu repositorio
- Verás el workflow "Deploy to GitHub Pages" ejecutándose
- Cuando termine (✅ check verde), tu sitio estará listo

### 5. Acceder a tu Presentación

Tu presentación estará disponible en:

```
https://TU_USUARIO.github.io/presentacion-unitree-go2/
```

## 🔄 Actualizaciones Futuras

Cada vez que hagas push a la rama `main`, GitHub Pages se actualizará automáticamente:

```bash
# Hacer cambios en el código
git add .
git commit -m "Actualización de contenido"
git push
```

## 📝 Notas Importantes

1. **Primera vez puede tardar 2-3 minutos** en estar disponible
2. **El sitio es público** - cualquiera puede verlo con el link
3. **Cache del navegador** - Si no ves cambios, prueba Ctrl+Shift+R
4. **Base path** - Ya está configurado en `vite.config.js`

## 🎯 Archivos Clave del Deploy

- `.github/workflows/deploy.yml` - Workflow de GitHub Actions
- `vite.config.js` - Configuración con base path
- `package.json` - Scripts de build

## ❓ Troubleshooting

### El sitio muestra 404

- Verifica que GitHub Pages esté configurado en "GitHub Actions"
- Espera 2-3 minutos después del primer push
- Revisa que el workflow haya terminado exitosamente

### Los estilos no cargan

- El `base` path en `vite.config.js` debe coincidir con el nombre del repo
- Actualmente está configurado como: `/presentacion-unitree-go2/`

### El workflow falla

- Revisa los logs en la pestaña Actions
- Verifica que todas las dependencias estén en `package.json`

## 🎨 Personalización

Si quieres cambiar el nombre del repositorio:

1. Cambia el nombre en GitHub (Settings → Rename)
2. Actualiza `base` en `vite.config.js`:
   ```js
   base: '/NUEVO_NOMBRE/',
   ```
3. Haz push de los cambios

---

**¡Listo para presentar! 🚀**
