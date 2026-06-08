#!/bin/bash

echo "🚀 Script de Deploy Rápido - GitHub Pages"
echo "=========================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "package.json" ]; then
    echo "❌ Error: Ejecuta este script desde la carpeta presentacion-proyecto"
    exit 1
fi

echo "📝 Ingresa tu usuario de GitHub:"
read -r GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "❌ Error: Debes ingresar un usuario de GitHub"
    exit 1
fi

echo ""
echo "🔧 Configurando repositorio remoto..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$GITHUB_USER/presentacion-unitree-go2.git"

echo ""
echo "📦 Verificando que todo esté commiteado..."
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Hay cambios sin commitear. Commiteando..."
    git add .
    git commit -m "Deploy to GitHub Pages"
fi

echo ""
echo "🚀 Subiendo código a GitHub..."
echo "Si te pide credenciales, usa tu username y Personal Access Token"
echo ""

if git push -u origin main; then
    echo ""
    echo "✅ ¡Código subido exitosamente!"
    echo ""
    echo "📝 Ahora sigue estos pasos:"
    echo "1. Ve a: https://github.com/$GITHUB_USER/presentacion-unitree-go2/settings/pages"
    echo "2. En 'Source', selecciona: 'GitHub Actions'"
    echo "3. Espera 1-2 minutos"
    echo "4. Tu presentación estará en:"
    echo "   🌐 https://$GITHUB_USER.github.io/presentacion-unitree-go2/"
    echo ""
else
    echo ""
    echo "❌ Error al subir el código"
    echo ""
    echo "Posibles soluciones:"
    echo "1. Verifica que creaste el repositorio en GitHub:"
    echo "   https://github.com/new"
    echo "2. Nombre del repo: presentacion-unitree-go2"
    echo "3. Si ya existe, intenta: git push -f origin main"
    exit 1
fi
