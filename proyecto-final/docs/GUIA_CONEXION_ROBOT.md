# 🤖 Guía de Conexión al Robot (SIN INTERNET)

**IMPORTANTE:** Una vez conectado a la WiFi del robot, NO tendrás internet.
Imprime o guarda esta guía antes de conectarte.

---

## ✅ PRE-REQUISITOS (Verificar ANTES de desconectarte)

1. **Robot Unitree encendido**
   - Presionar botón de encendido
   - Esperar el PITIDO (~30 segundos)
   - Robot debe estar en posición inicial

2. **Verificar que el robot está listo**
   - El robot debe haber emitido un pitido de inicio
   - Las luces deben estar estables (no parpadeando)
   - El robot debe estar quieto y estable

3. **Dependencias instaladas** (verificar antes)
   ```bash
   cd /Users/adrianbazaldua/Desktop/work/verano/prosp-poc/proyecto-final
   
   # Verificar Ollama
   ollama list | grep qwen2.5:3b
   
   # Sincronizar dependencias
   uv sync
   ```

---

## 🔌 PASOS PARA CONECTARSE

### Paso 1: Desconectarte de tu red actual
```
1. Ir a Configuración de WiFi (esquina superior derecha)
2. Desconectarte de la red actual
```

### Paso 2: Conectarte a la red del robot
```
1. Buscar red WiFi: Unitree_XXXXX
2. Conectar con la contraseña del robot
3. Esperar a que se conecte (círculo WiFi con candado)
```

### Paso 3: Verificar IP del robot
```bash
# Verificar que estás en la red correcta
ifconfig en0 | grep "inet "
# Deberías ver algo como: inet 192.168.12.XXX

# El robot siempre está en:
# IP: 192.168.12.1
```

---

## 🚀 INICIAR EL SISTEMA

### Opción A: Script automático (RECOMENDADO)
```bash
cd /Users/adrianbazaldua/Desktop/work/verano/prosp-poc/proyecto-final
./start_demo.sh
```

### Opción B: Comando manual
```bash
cd /Users/adrianbazaldua/Desktop/work/verano/prosp-poc/proyecto-final
unset VIRTUAL_ENV
uv run python robot_voice_controller.py
```

---

## 🔍 QUÉ HACER SI NO SE CONECTA

### Error: "Robot is not exposing a signaling port"

Este error significa que el robot no está listo para WebRTC. Intenta:

#### Solución 1: Reiniciar el robot
```
1. Apagar el robot (mantener botón presionado ~3 seg)
2. Esperar 10 segundos
3. Encender de nuevo (mantener botón presionado)
4. Esperar el PITIDO de inicio (~30 seg)
5. Volver a intentar conectar
```

#### Solución 2: Verificar modo del robot
```
Algunos robots Unitree necesitan estar en un modo específico:
- El robot debe estar en "modo normal" o "modo sport"
- Si tiene una app oficial de Unitree, úsala primero para verificar conectividad
```

#### Solución 3: Usar IP alternativa
```bash
# Algunos modelos usan IPs diferentes:
export UNITREE_ROBOT_IP="192.168.123.161"
./start_demo.sh

# O probar:
export UNITREE_ROBOT_IP="192.168.123.15"
./start_demo.sh
```

#### Solución 4: Verificar versión de firmware
```
El robot puede necesitar una actualización de firmware para soportar WebRTC.
Consulta la documentación de Unitree para tu modelo específico.
```

---

## 🎯 SI LOGRA CONECTARSE

Verás esto:
```
============================================================
🤖 CONECTANDO AL ROBOT UNITREE
============================================================
📡 IP: 192.168.12.1
✅ Conexión WebRTC establecida

⏳ Cargando Whisper 'base'...
✅ Whisper cargado

============================================================
🎙️  SISTEMA DE CONTROL POR VOZ ACTIVO
============================================================
...
✅ LISTO (Comando #1)
============================================================
🎤 Presiona ENTER para grabar o Q para salir: _
```

### Comandos de prueba (en orden):
1. **"modo normal"** - Inicializa el robot
2. **"ponte de pie"** - Levanta el robot
3. **"saluda"** - Levanta la pata
4. **"camina hacia adelante"** - Avanza
5. **"siéntate"** - Se sienta

---

## 🛑 PARA SALIR
```
1. Presiona Q + ENTER (salida controlada)
2. O Ctrl+C (salida inmediata)
```

---

## 📝 TROUBLESHOOTING COMÚN

### Problema: "No se detectó comando"
- Habla más claro y cerca del micrófono
- Asegúrate de dar permisos de micrófono a la terminal

### Problema: Robot no responde a comandos
- Verifica que el robot esté en "modo normal"
- Reinicia la conexión (Ctrl+C y volver a ejecutar)

### Problema: Robot se cae o pierde balance
- Dale más espacio (mínimo 3x3 metros)
- Asegúrate de que el piso sea plano
- Di "apaga los motores" para detenerlo en emergencia

---

## 🔧 ALTERNATIVA: Probar sin robot primero

Si el robot no conecta, puedes probar el sistema sin hardware:

```bash
# Probar transcripción de voz
uv run python voice_to_robot.py

# Simula comandos sin robot real
```

---

## 📞 INFORMACIÓN ADICIONAL

### Especificaciones del robot Go2
- Modelo: Unitree Go2
- Protocolo: WebRTC
- Puerto de señalización: 8081 o 9991
- Red: LocalAP (192.168.12.1)

### Biblioteca usada
- `unitree-webrtc-connect` (versión en pyproject.toml)
- Documentación: https://github.com/unitreerobotics/unitree_sdk2

---

## ✅ CHECKLIST FINAL

Antes de conectarte al robot:

- [ ] Robot encendido y con pitido de inicio
- [ ] Ollama corriendo (`ollama list`)
- [ ] Dependencias instaladas (`uv sync`)
- [ ] Micrófono funcionando
- [ ] Robot tiene espacio para moverse (3x3m)
- [ ] Esta guía guardada/impresa
- [ ] Terminal abierta en el directorio correcto

**COMANDO FINAL:**
```bash
cd /Users/adrianbazaldua/Desktop/work/verano/prosp-poc/proyecto-final && ./start_demo.sh
```

---

## 🎓 PARA LA DEMO CON EL PROFESOR

Si el robot no conecta durante la demo, tienes estas opciones:

### Plan A: Demo sin robot (simulación)
```bash
# Muestra el pipeline completo sin hardware
uv run python voice_to_robot.py
```
- Graba voz → Whisper transcribe → LLM genera JSON
- Todo funciona igual, solo simula la ejecución

### Plan B: Demo con video pregrabado
- Graba un video del robot funcionando antes
- Muestra el código en vivo + video de respaldo

### Plan C: Explicar el sistema
- Muestra el código del controlador
- Explica la arquitectura: Voz → Whisper → Ollama → WebRTC → Robot
- Muestra los logs de conexión y tool calls

**El valor está en el sistema, no solo en el robot físico.**

---

¡Buena suerte con la demo! 🚀
