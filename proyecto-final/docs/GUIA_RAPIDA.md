# 🤖 Guía Rápida - Control por Voz del Robot Unitree

## 📋 Antes de Empezar

### Requisitos:
- ✅ Robot Unitree encendido
- ✅ Conectado a la red WiFi del robot (LocalAP)
- ✅ Micrófono funcionando
- ✅ Dependencias instaladas

---

## 🚀 Flujo Completo de Inicio

### 1️⃣ Encender el Robot
```
1. Presiona el botón de encendido del robot
2. Espera el pitido de inicio (~30 segundos)
3. El robot se pondrá en posición inicial automáticamente
```

### 2️⃣ Conectarte a la WiFi del Robot
```
Red WiFi: Unitree_XXXXX (busca tu red específica)
Contraseña: (la que te dio Unitree)
IP del robot: 192.168.12.1 (default)
```

### 3️⃣ Iniciar el Sistema de Control
```bash
cd ~/Desktop/work/verano/prosp-poc
uv run python robot_voice_controller.py
```

Verás:
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
============================================================
✅ LISTO (Comando #1)
============================================================
🎤 Presiona ENTER para grabar o Q para salir: _
```

**Presionas ENTER**

```
🎙️  Micrófono ACTIVADO
⏺️ 🔴 GRABANDO... (presiona ENTER para DETENER)
```

**Hablas tu comando y presionas ENTER de nuevo**

```
⏹️  Grabación detenida (X.X segundos)
```

---

## 🎤 Comandos que Puedes Decir

### 🏃 MOVIMIENTOS BÁSICOS

| Di esto | El robot hará |
|---------|---------------|
| **"camina hacia adelante"** | Avanza ~2 segundos |
| **"muévete hacia atrás"** | Retrocede ~2 segundos |
| **"muévete a la izquierda"** | Se desplaza lateralmente a la izquierda |
| **"muévete a la derecha"** | Se desplaza lateralmente a la derecha |
| **"detente"** o **"para"** | Se detiene inmediatamente |

### 🔄 GIROS

| Di esto | El robot hará |
|---------|---------------|
| **"gira a la izquierda"** | Gira sobre su eje (izquierda) |
| **"gira a la derecha"** | Gira sobre su eje (derecha) |
| **"da la vuelta"** | Gira 180 grados |

### 🎭 ANIMACIONES

| Di esto | El robot hará |
|---------|---------------|
| **"ponte de pie"** | Se levanta si está sentado |
| **"siéntate"** | Se sienta |
| **"saluda"** o **"haz que el perro salude"** | Levanta la pata (saludo) |
| **"estírate"** | Hace stretch |
| **"baila"** | Hace una danza |

### 🎮 MOVIMIENTOS COMPUESTOS

| Di esto | El robot hará |
|---------|---------------|
| **"retrocede girando a la izquierda"** | Retrocede mientras gira |
| **"avanza girando a la derecha"** | Avanza mientras gira |

### ⚙️ MODOS

| Di esto | El robot hará |
|---------|---------------|
| **"activa el modo caminar"** o **"modo normal"** | Modo de caminar normal |
| **"activa el modo de acrobacias"** o **"modo ai"** | Modo acrobacias (cuidado!) |
| **"apaga los motores"** o **"modo seguro"** | Apaga motores (modo seguro) |

---

## 📝 Ejemplo de Sesión Completa

```
[Sistema] ✅ LISTO (Comando #1)
[Sistema] 🎤 Presiona ENTER para grabar o Q para salir: _

[Tú] (Presionas ENTER)

[Sistema] 🎙️  Micrófono ACTIVADO
[Sistema] ⏺️ 🔴 GRABANDO... (presiona ENTER para DETENER)

[Tú] "ponte de pie" (y presionas ENTER)

[Sistema] ⏹️  Grabación detenida (2.3 segundos)
[Sistema] 📝 Transcribiendo...
[Sistema] 💬 Comando: "ponte de pie"
[Sistema] 🤖 Generando comando para el robot...
[Sistema] 📋 Tool call: {"name": "perform_action", "arguments": {"action_name": "StandUp"}}
[Sistema] 🤖 EJECUTANDO: perform_action
[Sistema] ✅ Comando completado

[Sistema] ============================================================
[Sistema] ✅ LISTO (Comando #2)
[Sistema] 🎤 Presiona ENTER para grabar o Q para salir: _

[Tú] (Presionas ENTER)

[Sistema] 🎙️  Micrófono ACTIVADO
[Sistema] ⏺️ 🔴 GRABANDO... (presiona ENTER para DETENER)

[Tú] "camina hacia adelante" (y presionas ENTER)

[Sistema] ⏹️  Grabación detenida (1.8 segundos)
[Sistema] 📝 Transcribiendo...
[Sistema] 💬 Comando: "camina hacia adelante"
[Sistema] 🤖 EJECUTANDO: move_robot
[Sistema] ✅ Comando completado

[Sistema] ✅ LISTO (Comando #3)
[Sistema] 🎤 Presiona ENTER para grabar o Q para salir: _

[Tú] (Presionas Q + ENTER)

[Sistema] 🛑 Saliendo de forma segura...
[Sistema] 🔌 Cerrando conexión con el robot...
[Sistema] ✅ Sistema cerrado correctamente
```

---

## ⚡ Tips y Mejores Prácticas

### ✅ DO's (Hacer)

1. **Presiona ENTER cuando quieras dar un comando**
   - El micrófono solo se activa cuando tú lo decides
   - Presiona ENTER nuevamente cuando termines de hablar
   - Tú controlas la duración de la grabación

2. **Habla claro y sin prisa**
   - "camina hacia adelante" ✅
   - No grites, habla normal

3. **Espera a ver "LISTO"**
   - No presiones ENTER mientras ejecuta un comando
   - El sistema te avisa cuando está listo

3. **Usa comandos simples primero**
   - Empieza con "siéntate", "ponte de pie"
   - Prueba movimientos básicos antes que compuestos

4. **Dale espacio al robot**
   - Asegúrate de que tenga espacio para moverse
   - Especialmente para giros y movimientos laterales

5. **Empieza con "modo normal"**
   - Di "activa el modo caminar" al inicio
   - Esto asegura que esté listo para moverse

### ❌ DON'Ts (Evitar)

1. **No des comandos mientras ejecuta**
   - Espera a que termine el comando actual
   - Verás "EJECUTANDO" cuando esté ocupado

2. **No uses comandos ambiguos**
   - ❌ "ve para allá"
   - ✅ "camina hacia adelante"

3. **No muevas el robot manualmente mientras está activo**
   - Puede perder el balance
   - Si necesitas moverlo, di "apaga los motores" primero

4. **No uses comandos muy rápidos seguidos**
   - El robot necesita estabilizarse entre comandos
   - El sistema ya maneja esto automáticamente

---

## 🛑 Cómo Detener el Sistema

### Detener Suavemente (Recomendado):
```
1. Espera a ver "🎤 Presiona ENTER para grabar o Q para salir:"
2. Escribe: Q
3. Presiona ENTER
```

### Detener Inmediatamente:
```
Presiona Ctrl+C
```

El sistema:
1. Detecta la interrupción
2. Detiene el movimiento actual
3. Cierra la conexión de forma segura
4. Muestra: "✅ Sistema cerrado correctamente"

### Emergencia (Robot descontrolado):
```
1. Presiona Ctrl+C en la terminal
2. Si no funciona: Desconecta el WiFi de tu laptop
3. Último recurso: Botón de apagado físico del robot
```

---

## 🔧 Troubleshooting

### "❌ No se pudo conectar al robot"
- Verifica que estés conectado al WiFi del robot
- Confirma la IP: `ping 192.168.12.1`
- Reinicia el robot

### "⚠️ No se detectó comando"
- Habla más claro
- Acércate más al micrófono
- Verifica que tu micrófono funciona: `uv run python test_whisper.py`

### "❌ No se pudo generar comando válido"
- Usa comandos de la lista de arriba
- Evita comandos muy complejos
- Reformula el comando de manera más simple

### "Robot no responde a comandos"
- Di "activa el modo caminar" primero
- Verifica que el robot esté en modo normal
- Reinicia la conexión (Ctrl+C y volver a correr)

---

## 📊 Secuencia de Prueba Recomendada

Para tu primera sesión, prueba esta secuencia:

```
1. "activa el modo caminar"          # Inicializar modo
2. "ponte de pie"                     # Asegurar que esté parado
3. "saluda"                           # Animación simple
4. "camina hacia adelante"            # Movimiento básico
5. "detente"                          # Detener
6. "gira a la derecha"                # Giro simple
7. "muévete a la izquierda"           # Movimiento lateral
8. "siéntate"                         # Animación final
9. "apaga los motores"                # Modo seguro para finalizar
```

---

## 🎯 Resumen Ultra-Rápido

```
1. Enciende robot → Espera pitido
2. Conecta WiFi → 192.168.12.1
3. Ejecuta: uv run python robot_voice_controller.py
4. Espera "✅ LISTO"
5. Presiona ENTER → Habla tu comando → Presiona ENTER de nuevo
6. Espera que ejecute
7. Repite desde paso 4
8. Para salir: Q + ENTER (o Ctrl+C)
```

**Comandos más útiles:**
- "camina hacia adelante" / "atrás"
- "gira a la izquierda" / "derecha"
- "detente"
- "siéntate" / "ponte de pie"
- "saluda"

¡Listo para controlar tu robot por voz! 🤖🎙️
