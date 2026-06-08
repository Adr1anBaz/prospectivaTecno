# 🎯 DEMO RÁPIDA - Guía de Inicio (3 minutos)

## ✅ Pre-requisitos (Verificar antes de la demo)

### 1. Robot Unitree
- ✅ Robot encendido (esperar pitido ~30 seg)
- ✅ Robot en posición inicial

### 2. Conectar a WiFi del Robot
```bash
# Buscar red WiFi: Unitree_XXXXX
# IP del robot: 192.168.12.1
```

### 3. Dependencias del Sistema
```bash
# ✅ Ollama está corriendo
# ✅ uv está instalado
# ✅ Modelo qwen2.5:3b instalado (1.9 GB)
```

---

## 🚀 INICIO RÁPIDO (2 pasos)

### Paso 1: Ir al directorio del proyecto
```bash
cd /Users/adrianbazaldua/Desktop/work/verano/prosp-poc/proyecto-final
```

### Paso 2: Ejecutar el controlador
```bash
uv run python robot_voice_controller.py
```

---

## 📝 Lo que verás al iniciar

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
Modelo LLM: qwen2.5:3b
Modelo Whisper: base

💡 Comandos de voz disponibles:
   • Movimiento: 'camina adelante', 'gira a la derecha'
   • Animaciones: 'siéntate', 'saluda', 'baila'
   • Modos: 'modo normal', 'apaga motores'
   • Control: 'detente', 'para'

⌨️  Control del sistema:
   • ENTER → Activar micrófono (inicio de grabación)
   • ENTER nuevamente → Detener grabación
   • Q + ENTER → Salir de forma segura
============================================================

============================================================
✅ LISTO (Comando #1)
============================================================
🎤 Presiona ENTER para grabar o Q para salir: _
```

---

## 🎤 COMANDOS PARA LA DEMO (en orden recomendado)

### Secuencia de Demo Profesional (5 comandos)

1. **"modo normal"**
   - Inicializa el robot para movimiento
   - Duración: ~3 seg

2. **"ponte de pie"**
   - El robot se levanta si está sentado
   - Duración: ~3 seg

3. **"saluda"**
   - El robot levanta la pata (animación impresionante)
   - Duración: ~3 seg

4. **"camina hacia adelante"**
   - El robot avanza ~2 metros
   - Duración: ~2 seg

5. **"siéntate"**
   - El robot se sienta (pose final)
   - Duración: ~3 seg

**Tiempo total: ~14 segundos + grabaciones (30-45 segundos total)**

---

## 🎯 CÓMO DAR CADA COMANDO

```
1. Sistema muestra: ✅ LISTO (Comando #1)
   🎤 Presiona ENTER para grabar o Q para salir: _

2. TÚ presionas: ENTER

3. Sistema muestra: 🎙️  Micrófono ACTIVADO
                    ⏺️ 🔴 GRABANDO... (presiona ENTER para DETENER)

4. TÚ dices: "ponte de pie"  (claro y sin prisa)

5. TÚ presionas: ENTER (para detener)

6. Sistema muestra: ⏹️  Grabación detenida (X.X segundos)
                    📝 Transcribiendo...
                    💬 Comando: "ponte de pie"
                    🤖 Generando comando para el robot...
                    📋 Tool call: {...}
                    🤖 EJECUTANDO: perform_action
                    ✅ Comando completado

7. Repite desde el paso 1 para el siguiente comando
```

---

## ⚡ TROUBLESHOOTING RÁPIDO

### Si el robot no se conecta:
```bash
# Verificar que estás en la red WiFi del robot
# Verificar IP del robot
ping 192.168.12.1

# Si no responde, verificar variable de entorno
export UNITREE_ROBOT_IP="192.168.12.1"
```

### Si Ollama no responde:
```bash
# Verificar que Ollama está corriendo
ollama list

# Si no está corriendo, iniciarlo
brew services start ollama
```

### Si el micrófono no funciona:
```bash
# macOS pedirá permiso la primera vez
# Ir a: Configuración del Sistema > Privacidad y Seguridad > Micrófono
# Permitir acceso a Terminal o tu IDE
```

---

## 🛑 PARA SALIR

### Opción 1: Salida controlada (Recomendado)
```
1. Espera a ver: "🎤 Presiona ENTER para grabar o Q para salir: _"
2. Escribe: Q
3. Presiona: ENTER
```

### Opción 2: Salida inmediata
```
Presiona: Ctrl+C
```

El sistema automáticamente:
- Detiene el robot
- Cierra la conexión WebRTC
- Muestra: "✅ Sistema cerrado correctamente"

---

## 💡 TIPS PARA UNA DEMO EXITOSA

1. **Habla claro pero natural**
   - No grites
   - Pronuncia bien cada palabra
   - No hay prisa

2. **Dale espacio al robot**
   - Al menos 2-3 metros para movimientos
   - Asegúrate de que no hay obstáculos

3. **Espera entre comandos**
   - El sistema te dirá cuando está "LISTO"
   - No presiones ENTER mientras ejecuta

4. **Si algo sale mal**
   - Ctrl+C detiene todo
   - Puedes volver a ejecutar el script

5. **Para impresionar al profesor**
   - Muestra el flujo: Voz → Whisper → LLM → Comando JSON → Robot
   - Explica los guardrails de seguridad
   - Menciona que es 100% local (sin internet)

---

## 🎬 SCRIPT DE PRESENTACIÓN (30 segundos)

```
"Este es un sistema de control por voz para el robot Unitree Go2.

El sistema usa Whisper para transcribir mi voz a texto,
luego un modelo LLM local (Qwen 2.5) genera comandos JSON
usando tool calling, y finalmente los ejecuta en el robot.

Todo es 100% local, sin necesidad de internet.

Déjame demostrarlo..."

[Presionar ENTER]
[Decir: "ponte de pie"]
[Presionar ENTER]

"Como pueden ver, el robot interpretó mi comando correctamente
y se puso de pie. Puedo dar comandos más complejos..."

[Siguiente comando...]
```

---

## ✅ CHECKLIST PRE-DEMO

- [ ] Robot encendido (escuchaste el pitido)
- [ ] Conectado a WiFi Unitree_XXXXX
- [ ] `ping 192.168.12.1` responde
- [ ] Terminal abierta en el directorio correcto
- [ ] Micrófono funcionando
- [ ] Robot tiene espacio para moverse
- [ ] Script de presentación preparado

---

## 🚀 COMANDO FINAL

```bash
cd /Users/adrianbazaldua/Desktop/work/verano/prosp-poc/proyecto-final && uv run python robot_voice_controller.py
```

**¡Buena suerte con la demo! 🎉**
