# 🚀 Inicio Rápido

Guía rápida para empezar a trabajar en este repositorio.

## 📂 Estructura

```
prosp-poc/
├── proyecto-final/     → 🤖 Control de robot por voz (Whisper + Ollama + Unitree)
└── practicas/
    └── practica-1/     → 📚 Panorama de IA Generativa y LLM (Ollama)
```

---

## 🤖 Proyecto Final

**¿Qué es?** Sistema de control por voz para robot Unitree con 100% de precisión.

### Setup Rápido

```bash
cd proyecto-final
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
ollama pull llama3.2
```

### Ejecutar

```bash
python robot_voice_controller.py
# Presiona ESPACIO → Habla → Suelta
```

📖 [README completo](./proyecto-final/README.md)

---

## 📚 Práctica 1: Ollama y LLMs

**¿Qué es?** Exploración práctica de 6 modelos LLM usando Ollama.

### Setup Rápido

```bash
# 1. Instalar Ollama
brew install ollama  # macOS
brew services start ollama

# 2. Setup del proyecto
cd practicas/practica-1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# 3. Descargar modelos (mínimo 6)
ollama pull llama3.2:3b
ollama pull gemma2:2b
ollama pull qwen2.5:7b
ollama pull mistral:7b
ollama pull phi4
ollama pull tinyllama

# 4. Verificar
ollama list
```

### Ejecutar Práctica

```bash
# Opción 1: Script automático
python scripts/ejecutar_modelos.py

# Opción 2: Manual
ollama run llama3.2:3b "¿Qué es la IA?"
ollama run gemma2:2b "¿Qué es la IA?"
# ... (mismo prompt para todos)
```

### Entregables

1. ✅ Capturas de descargas → `descargas/`
2. ✅ Capturas de ejecuciones → `ejecuciones/`
3. ✅ Tabla comparativa → `comparativa.md`
4. ✅ Reflexión → `reflexion.md`

📖 [README completo](./practicas/practica-1/README.md)

---

## 🔧 Comandos Útiles

### Git

```bash
# Ver estructura
tree -L 2 -I '.venv|__pycache__'

# Estado
git status

# Commit
git add .
git commit -m "Completar práctica 1"
```

### Ollama

```bash
ollama list                    # Ver modelos instalados
ollama run modelo:tag          # Ejecutar modelo interactivo
ollama pull modelo:tag         # Descargar modelo
ollama rm modelo:tag           # Eliminar modelo
ollama show modelo:tag         # Info del modelo
```

### Entornos Virtuales

```bash
# Activar
source .venv/bin/activate

# Desactivar
deactivate

# Verificar activo
which python
echo $VIRTUAL_ENV
```

---

## 🆘 Solución de Problemas

### "No module named X"
```bash
# Asegúrate de estar en el entorno correcto
which python  # Debe mostrar ruta con .venv

# Reinstalar dependencias
pip install -e .
```

### "ollama: command not found"
```bash
# Instalar Ollama
brew install ollama
brew services start ollama

# Verificar
ollama --version
```

### "No puedo grabar audio"
- macOS: Permisos del sistema → Seguridad → Privacidad → Micrófono
- Habilita Terminal o tu IDE

---

## 📚 Documentación Completa

- [README General](./README.md) - Visión general del repositorio
- [SETUP.md](./SETUP.md) - Configuración detallada de entornos
- [Proyecto Final](./proyecto-final/README.md) - Documentación del robot
- [Práctica 1](./practicas/practica-1/README.md) - Instrucciones de la práctica

---

## ⚡ Atajos

| Tarea | Comando |
|-------|---------|
| Ver modelos Ollama | `ollama list` |
| Ejecutar Proyecto Final | `cd proyecto-final && source .venv/bin/activate && python robot_voice_controller.py` |
| Ejecutar Práctica 1 | `cd practicas/practica-1 && source .venv/bin/activate && python scripts/ejecutar_modelos.py` |
| Ver info de modelo | `python scripts/info_modelos.py` |
| Probar Whisper | `cd proyecto-final && python test_whisper.py` |

---

**Autor:** Adrian Bazaldua  
**Última actualización:** 2026-06-01
