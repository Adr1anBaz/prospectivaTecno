<<<<<<< HEAD
# 🤖 Presentación del Proyecto Unitree Go2

Presentación interactiva y dinámica sobre el sistema de control inteligente para el robot Unitree Go2 Air.

## 🚀 Características

- ✅ **Control por Voz** - Sistema local con Whisper y Ollama
- ✅ **Telemetría en Tiempo Real** - Dashboard completo de sensores
- ✅ **Navegación Autónoma** - ROS2 + SLAM Toolbox + Nav2
- ✅ **Animaciones Fluidas** - Transiciones con Framer Motion
- ✅ **Diseño Moderno** - UI glassmorphism con degradados

## 📦 Instalación Local

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview
```

## 🎯 Navegación

- **Flechas del teclado** o **clic en botones** para navegar
- **Espacio** para avanzar
- **Indicadores** en la parte inferior para saltar a slides específicas

## 📑 Contenido

1. **Introducción** - Overview del proyecto
2. **Control por Voz** - Pipeline de procesamiento y comandos
3. **Arquitectura** - Stack tecnológico y flujo de datos
4. **Telemetría** - Datos monitoreados en tiempo real
5. **ROS2 & SLAM** - Sistema de navegación autónoma
6. **Desafíos** - Problemas y soluciones propuestas
7. **Demo** - Ejemplos de uso y casos de prueba
8. **Próximos Pasos** - Roadmap y visión futura

## 🌐 Deploy en GitHub Pages

Esta aplicación está configurada para deployarse automáticamente en GitHub Pages.

### Pasos para Deploy

1. **Crear repositorio en GitHub**
   ```bash
   # Cambiar 'username' por tu usuario de GitHub
   git remote add origin https://github.com/username/presentacion-unitree-go2.git
   ```

2. **Subir código**
   ```bash
   git add .
   git commit -m "Deploy: Presentación Unitree Go2"
   git push -u origin main
   ```

3. **Configurar GitHub Pages**
   - Ve a: `Settings` → `Pages`
   - Source: `GitHub Actions`
   - El workflow se ejecutará automáticamente

4. **Acceder a la presentación**
   - URL: `https://username.github.io/presentacion-unitree-go2/`

### Deploy Manual

```bash
npm run build
# Los archivos generados están en /dist
```

## 🛠️ Stack Tecnológico

- **React 18** - Framework UI
- **Vite 4** - Build tool
- **Framer Motion 10** - Animaciones
- **CSS3** - Estilos modernos

## 📄 Licencia

Proyecto de investigación y desarrollo
=======
# Repositorio de IA y Robótica - Verano 2026

Este repositorio contiene el proyecto final y las prácticas del curso de IA Generativa y LLMs.

## Estructura del Repositorio

```
.
├── proyecto-final/     # Proyecto final: Control por voz de robot Unitree
│   ├── .venv/          # Entorno virtual del proyecto
│   └── ...             # Código fuente del proyecto
│
└── practicas/          # Prácticas del curso
    ├── practica-1/     # Panorama de IA generativa y LLM (Ollama)
    └── ...             # Otras prácticas
```

## Proyecto Final

Sistema de control por voz para robot Unitree con precisión del 100% en llamadas de herramientas usando Whisper y Ollama.

📁 [Ver Proyecto Final](./proyecto-final/)

## Prácticas

### Práctica 1: Panorama de IA Generativa y LLM

Exploración de modelos de lenguaje usando Ollama y Hugging Face.

📁 [Ver Práctica 1](./practicas/practica-1/)

## Instalación

Cada carpeta (proyecto-final y cada práctica) tiene su propio entorno virtual independiente. 

Ver los README específicos en cada carpeta para instrucciones de instalación.

## Requisitos Generales

- Python 3.9+
- uv (gestor de paquetes)
- Ollama (para LLMs locales)

## Autor

Adrian Bazaldua
>>>>>>> e21da9bcef627ef9c8a55b2ca790f6c5f0153345
