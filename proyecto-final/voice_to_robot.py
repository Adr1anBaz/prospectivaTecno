#!/usr/bin/env python3
"""
Pipeline completo: Voz → Whisper → Ollama (Tool Calling) → Comando Robot
Optimizado para modelos pequeños (<1B parámetros)
"""

import whisper
import sounddevice as sd
import numpy as np
import ollama
import json
import sys
from robot_tools import (
    SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES,
    validate_tool_call
)


def record_audio_interactive(sample_rate: int = 16000):
    """
    Graba audio del micrófono de manera interactiva

    Returns:
        numpy array con el audio grabado
    """
    print("\n" + "="*60)
    print("🎤 GRABACIÓN DE COMANDO")
    print("="*60)
    print("\n📝 Presiona ENTER para empezar a grabar...")
    input()

    print("\n⏺️  🔴 GRABANDO... (presiona ENTER para detener)")
    print("💬 Di tu comando de voz ahora...")

    audio_chunks = []

    def callback(indata, frames, time, status):
        if status:
            print(f"⚠️  {status}", file=sys.stderr)
        audio_chunks.append(indata.copy())

    try:
        stream = sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype='float32',
            callback=callback
        )

        with stream:
            input()

        print("\n⏹️  Grabación detenida")

        if audio_chunks:
            audio_data = np.concatenate(audio_chunks, axis=0)
            duration = len(audio_data) / sample_rate
            print(f"✅ Audio capturado: {duration:.1f} segundos")
            return audio_data, sample_rate
        else:
            print("❌ No se grabó audio")
            return None, sample_rate

    except KeyboardInterrupt:
        print("\n\n⚠️  Grabación cancelada")
        return None, sample_rate
    except Exception as e:
        print(f"\n❌ Error durante la grabación: {e}")
        return None, sample_rate


def transcribe_command(audio_data, sample_rate, model_size="base"):
    """
    Transcribe el comando de voz usando Whisper

    Returns:
        Texto transcrito o None
    """
    print("\n" + "="*60)
    print("📝 TRANSCRIPCIÓN")
    print("="*60)

    print(f"\n⏳ Cargando Whisper '{model_size}'...")

    try:
        model = whisper.load_model(model_size)
        print("✅ Whisper cargado")
        print("⏳ Transcribiendo comando...")

        audio_flat = audio_data.flatten().astype(np.float32)
        result = model.transcribe(audio_flat, language="es", fp16=False)

        transcription = result["text"].strip()

        if not transcription:
            print("⚠️  No se detectó texto")
            return None

        print("\n✅ Transcripción completada")
        print(f"💬 Comando: \"{transcription}\"")

        return transcription

    except Exception as e:
        print(f"\n❌ Error al transcribir: {e}")
        return None


def generate_tool_call(command: str, model_name="qwen2.5:1.5b"):
    """
    Genera un tool call JSON usando Ollama

    Args:
        command: Comando transcrito en texto
        model_name: Modelo de Ollama a usar

    Returns:
        dict con tool call o None si hay error
    """
    print("\n" + "="*60)
    print("🤖 GENERACIÓN DE COMANDO")
    print("="*60)

    print(f"\n⏳ Preparando modelo {model_name}...")

    try:
        # Construir mensajes con few-shot examples
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        messages.extend(FEW_SHOT_EXAMPLES)
        messages.append({"role": "user", "content": command})

        print("⏳ Modelo procesando comando...")
        print("💭 Generando tool call JSON...\n")

        # Llamar a Ollama con configuración estricta
        response = ollama.chat(
            model=model_name,
            messages=messages,
            options={
                "temperature": 0.0,      # Determinista al 100%
                "top_k": 10,
                "top_p": 0.9,
                "num_predict": 60,       # Max tokens (un JSON nunca será más largo)
                "repeat_penalty": 1.1
            },
            format="json"  # Forzar output JSON
        )

        json_string = response['message']['content'].strip()

        print("="*60)
        print("📋 TOOL CALL GENERADO")
        print("="*60)
        print(json_string)
        print("="*60)

        # Parsear JSON
        tool_call = json.loads(json_string)

        # Validar con guardrails
        is_valid, error_msg = validate_tool_call(tool_call)

        if not is_valid:
            print(f"\n⚠️  GUARDRAIL ACTIVADO: {error_msg}")
            print("🛡️  Comando bloqueado por seguridad")
            return None

        print("\n✅ Tool call válido y seguro")

        return tool_call

    except json.JSONDecodeError as e:
        print(f"\n❌ Error: El modelo no generó JSON válido")
        print(f"   Respuesta cruda: {json_string[:200]}")
        return None
    except Exception as e:
        print(f"\n❌ Error al generar tool call: {e}")
        return None


def execute_tool_call_mock(tool_call: dict):
    """
    Simula la ejecución del comando (sin robot real)

    Args:
        tool_call: Diccionario con name y arguments
    """
    print("\n" + "="*60)
    print("🤖 EJECUCIÓN (MODO SIMULACIÓN)")
    print("="*60)

    name = tool_call.get("name")
    args = tool_call.get("arguments", {})

    print(f"\n🔧 Tool: {name}")
    print(f"📊 Argumentos: {json.dumps(args, indent=2)}")

    # Simular diferentes tipos de comandos
    if name == "move_robot":
        x, y, z = args.get("x", 0), args.get("y", 0), args.get("z", 0)
        direction = []
        if x > 0:
            direction.append("adelante")
        elif x < 0:
            direction.append("atrás")
        if y > 0:
            direction.append("izquierda")
        elif y < 0:
            direction.append("derecha")
        if z > 0:
            direction.append("giro izquierda")
        elif z < 0:
            direction.append("giro derecha")

        print(f"\n🐕 Robot moviéndose: {' + '.join(direction) if direction else 'detenido'}")

    elif name == "perform_action":
        action = args.get("action_name")
        print(f"\n🎭 Robot ejecutando: {action}")

    elif name == "change_mode":
        mode = args.get("mode_name")
        print(f"\n⚙️  Robot cambiando a modo: {mode}")

    print("\n✅ Comando ejecutado exitosamente (simulado)")


def main():
    """Función principal"""
    print("="*60)
    print("🎙️  VOICE TO ROBOT COMMAND")
    print("="*60)
    print("\n🤖 Pipeline completo:")
    print("  1️⃣  Grabar comando de voz")
    print("  2️⃣  Transcribir con Whisper")
    print("  3️⃣  Generar tool call con Ollama")
    print("  4️⃣  Validar con guardrails")
    print("  5️⃣  Ejecutar comando (simulado)")
    print("\n" + "="*60)

    # Configuración
    WHISPER_MODEL = "base"
    LLM_MODEL = "qwen2.5:3b"  # Opciones: qwen2.5:0.5b, qwen2.5:1.5b, qwen2.5:3b (recomendado)

    # Permitir override del modelo via CLI
    if len(sys.argv) > 1:
        LLM_MODEL = sys.argv[1]
        print(f"\n🤖 Usando modelo: {LLM_MODEL}")

    # Paso 1: Grabar comando
    audio_data, sample_rate = record_audio_interactive()
    if audio_data is None:
        print("\n❌ No se pudo grabar audio. Abortando.")
        sys.exit(1)

    # Paso 2: Transcribir
    command = transcribe_command(audio_data, sample_rate, WHISPER_MODEL)
    if not command:
        print("\n❌ No se pudo transcribir comando. Abortando.")
        sys.exit(1)

    # Paso 3: Generar tool call
    tool_call = generate_tool_call(command, LLM_MODEL)
    if not tool_call:
        print("\n❌ No se pudo generar comando válido.")
        sys.exit(1)

    # Paso 4: Ejecutar (simulado)
    execute_tool_call_mock(tool_call)

    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO")
    print("="*60)
    print("\n💡 Pipeline funcionando correctamente")
    print("   • Voz → Whisper → Texto")
    print("   • Texto → Ollama → Tool Call JSON")
    print("   • Tool Call → Guardrails → Comando Seguro")
    print("\n🚀 Listo para conectar al robot real")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido")
        sys.exit(0)
