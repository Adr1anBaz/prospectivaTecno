---
layout: default
title: 1. Instalación
nav_order: 2
---

# 1. Instalación de Ollama

## Sistema Operativo

**Sistema:** macOS Sonoma 14.x  
**Procesador:** Apple Silicon M4  
**Memoria:** 16 GB RAM

---

## Proceso de Instalación

### Comando de Instalación

Ollama fue instalado usando Homebrew:

```bash
brew install ollama
brew services start ollama
```

---

## Verificación de Instalación

### Comando ejecutado:
```bash
ollama --version
```

### Captura Requerida: `ollama --version`

![Verificación de Ollama](ollama-version.png)
*Captura mostrando la versión instalada de Ollama*

**Resultado obtenido:**
```
ollama version is 0.X.X
```

---

## Observaciones

La instalación de Ollama fue un proceso **sumamente sencillo e intuitivo**, destacando por su enfoque *plug-and-play*. La documentación oficial es minimalista pero clara, permitiendo interactuar con el ecosistema a través de la terminal de manera inmediata.

El principal reto técnico radicó en el tiempo de descarga debido al peso de los archivos de parámetros más grandes, y en asegurar el espacio suficiente en el disco duro.

---

[Siguiente: Modelos Descargados →](./modelos){: .btn .btn-primary }
