# Guía de Configuración del Repositorio

Este repositorio contiene múltiples proyectos con entornos virtuales independientes.

## Estructura

```
prosp-poc/
├── proyecto-final/        # Proyecto final: Control de robot por voz
│   ├── .venv/             # Entorno virtual independiente
│   ├── pyproject.toml     # Dependencias del proyecto
│   └── ...
│
└── practicas/             # Prácticas del curso
    └── practica-1/        # Práctica 1: Ollama y LLM
        ├── .venv/         # Entorno virtual independiente
        ├── pyproject.toml # Dependencias de la práctica
        └── ...
```

## Configuración de Entornos Virtuales

Cada carpeta tiene su propio entorno virtual para evitar conflictos de dependencias.

### Proyecto Final

```bash
# Navegar al proyecto
cd proyecto-final

# Crear entorno virtual (si no existe)
python3 -m venv .venv

# Activar entorno
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows

# Instalar dependencias con uv
uv pip install -e .

# O con pip regular
pip install -e .

# Verificar instalación
python test_whisper.py
```

**Dependencias principales:**
- openai-whisper (transcripción)
- torch (ML backend)
- sounddevice (audio)
- ollama (LLM local)
- unitree-webrtc-connect (robot)

### Práctica 1

```bash
# Navegar a la práctica
cd practicas/practica-1

# Crear entorno virtual (si no existe)
python3 -m venv .venv

# Activar entorno
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -e .

# Verificar instalación
python scripts/info_modelos.py
```

**Dependencias principales:**
- ollama (cliente Python)
- huggingface-hub (consulta de modelos)

## Gestión de Entornos

### Cambiar entre Proyectos

```bash
# Desactivar entorno actual
deactivate

# Ir al otro proyecto
cd ../proyecto-final  # o ../practicas/practica-1

# Activar su entorno
source .venv/bin/activate
```

### Verificar Entorno Activo

```bash
# Ver ruta del entorno
which python

# Debe mostrar:
# /ruta/proyecto-final/.venv/bin/python
# o
# /ruta/practicas/practica-1/.venv/bin/python
```

### Listar Paquetes Instalados

```bash
# Con pip
pip list

# Con uv
uv pip list
```

## Requisitos del Sistema

### Común para Ambos

- **Python:** 3.9 o superior
- **Ollama:** Instalado localmente
  ```bash
  # macOS
  brew install ollama
  brew services start ollama
  
  # Linux
  curl -fsSL https://ollama.com/install.sh | sh
  ```

### Proyecto Final Adicional

- **Torch:** Se instala automáticamente
- **ffmpeg:** Para algunos formatos de audio (opcional)
  ```bash
  brew install ffmpeg  # macOS
  sudo apt install ffmpeg  # Linux
  ```

## Solución de Problemas

### Conflictos de Dependencias

Si encuentras conflictos, asegúrate de estar en el entorno correcto:

```bash
# Ver entorno activo
echo $VIRTUAL_ENV

# Debe coincidir con el proyecto actual
# Ejemplo: /Users/tu-usuario/.../proyecto-final/.venv
```

### Reinstalar Entorno

Si algo sale mal, puedes recrear el entorno:

```bash
# Desactivar
deactivate

# Eliminar entorno
rm -rf .venv

# Recrear
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Permisos de Micrófono (macOS)

La primera vez que ejecutes scripts de audio, macOS pedirá permisos:

1. Ve a **Preferencias del Sistema** > **Seguridad y Privacidad** > **Privacidad**
2. Selecciona **Micrófono**
3. Habilita **Terminal** o tu editor de código

## Mejores Prácticas

1. **Siempre activa el entorno** antes de trabajar en un proyecto
2. **Verifica el entorno activo** con `which python`
3. **No instales dependencias globalmente** - usa el entorno virtual
4. **Cada proyecto es independiente** - no comparten paquetes
5. **Lee el README** de cada carpeta para instrucciones específicas

## Scripts Útiles

### Verificar Configuración

```bash
# Desde la raíz del repositorio
# Verifica ambos entornos

echo "=== Proyecto Final ==="
cd proyecto-final
if [ -d ".venv" ]; then
    source .venv/bin/activate
    python --version
    pip list | grep -E "whisper|ollama|torch"
    deactivate
else
    echo "❌ Entorno no configurado"
fi

echo -e "\n=== Práctica 1 ==="
cd ../practicas/practica-1
if [ -d ".venv" ]; then
    source .venv/bin/activate
    python --version
    pip list | grep -E "ollama|huggingface"
    deactivate
else
    echo "❌ Entorno no configurado"
fi
```

## Recursos

- [Documentación de venv](https://docs.python.org/3/library/venv.html)
- [Guía de uv](https://github.com/astral-sh/uv)
- [Ollama Docs](https://ollama.com/docs)
- [Whisper OpenAI](https://github.com/openai/whisper)

---

**Última actualización:** 2026-06-01  
**Autor:** Adrian Bazaldua
