# ✅ Checklist de Deploy - GitHub Pages

## Pre-Deploy

- [x] Proyecto React creado y funcionando
- [x] Build de producción exitoso (`npm run build`)
- [x] Configuración de Vite con base path correcto
- [x] GitHub Actions workflow configurado
- [x] Git inicializado con commits
- [x] Documentación completa (README, instrucciones)
- [x] Script de deploy automático creado

## Deploy Steps

### 1. Crear Repositorio en GitHub

- [ ] Ve a https://github.com/new
- [ ] Nombre: `presentacion-unitree-go2`
- [ ] Visibilidad: **Público** ✅
- [ ] NO inicializar con README/gitignore/licencia
- [ ] Click en "Create repository"

### 2. Conectar Repositorio Local

**OPCIÓN A - Script Automático (Recomendado):**

```bash
cd presentacion-proyecto
./QUICK_DEPLOY.sh
# Sigue las instrucciones en pantalla
```

**OPCIÓN B - Manual:**

```bash
cd presentacion-proyecto

# Reemplaza TU_USUARIO con tu username de GitHub
git remote add origin https://github.com/TU_USUARIO/presentacion-unitree-go2.git

# Push del código
git push -u origin main
```

### 3. Configurar GitHub Pages

- [ ] Ve a tu repositorio en GitHub
- [ ] Click en **Settings** (arriba derecha)
- [ ] En el menú lateral izquierdo, click en **Pages**
- [ ] En "Build and deployment":
  - [ ] Source: Selecciona **GitHub Actions** ✅
- [ ] Guarda los cambios

### 4. Verificar Deployment

- [ ] Ve a la pestaña **Actions** en tu repositorio
- [ ] Verifica que el workflow "Deploy to GitHub Pages" esté corriendo
- [ ] Espera a que termine (icono ✅ verde)
- [ ] Click en el workflow para ver los detalles

### 5. Acceder a tu Presentación

Tu sitio estará disponible en:
```
https://TU_USUARIO.github.io/presentacion-unitree-go2/
```

- [ ] Abre el link en tu navegador
- [ ] Verifica que carga correctamente
- [ ] Prueba la navegación entre slides
- [ ] Verifica que los estilos se vean bien

## Troubleshooting

### ❌ Si el sitio muestra 404

- [ ] Verifica que GitHub Pages esté en modo "GitHub Actions"
- [ ] Espera 2-3 minutos más (primera vez puede tardar)
- [ ] Refresca la página con Ctrl+Shift+R (borrar cache)
- [ ] Verifica que el workflow terminó exitosamente en Actions

### ❌ Si los estilos no cargan

- [ ] Verifica que `vite.config.js` tenga: `base: '/presentacion-unitree-go2/'`
- [ ] Verifica que el nombre del repo coincida con el base path
- [ ] Re-build y re-push si hiciste cambios

### ❌ Si el workflow falla

- [ ] Ve a Actions y click en el workflow fallido
- [ ] Revisa los logs de error
- [ ] Verifica que `package.json` tenga todas las dependencias
- [ ] Verifica que el build local funcione: `npm run build`

## Post-Deploy

### Verificaciones Finales

- [ ] Presentación carga correctamente
- [ ] Las 8 slides se muestran
- [ ] Navegación con flechas funciona
- [ ] Navegación con clicks funciona
- [ ] Animaciones son fluidas
- [ ] Responsive (prueba en móvil)
- [ ] Comparte el link con tu equipo

### Actualizaciones Futuras

Para actualizar la presentación:

```bash
# Hacer cambios en el código
git add .
git commit -m "Descripción de los cambios"
git push

# GitHub Actions desplegará automáticamente
```

## 📝 URLs Importantes

- **Repositorio:** `https://github.com/TU_USUARIO/presentacion-unitree-go2`
- **Presentación:** `https://TU_USUARIO.github.io/presentacion-unitree-go2/`
- **Actions:** `https://github.com/TU_USUARIO/presentacion-unitree-go2/actions`
- **Settings:** `https://github.com/TU_USUARIO/presentacion-unitree-go2/settings/pages`

## 🎉 ¡Listo!

Una vez completado este checklist, tu presentación estará live y accesible públicamente.

**Comparte el link:**
```
https://TU_USUARIO.github.io/presentacion-unitree-go2/
```

---

**Tiempo estimado total:** 5-10 minutos
**Primera carga del sitio:** 1-3 minutos después del push
