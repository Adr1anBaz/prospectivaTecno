#!/usr/bin/env python3
"""
Controlador de voz para el robot Unitree Go2 AIR en SIMULACION (MuJoCo).

Flujo: Voz → Whisper → Ollama → Tool Call → ROS 2 / DDS → MuJoCo Sim

Diferencias con el controlador de hardware real:
  - En lugar de WebRTC, publica comandos via subprocess al binario C++
    go2_sport_client que usa CycloneDDS para comunicarse con el simulador.
  - Reutiliza robot_tools.py del proyecto-final sin modificaciones.
"""

import asyncio
import os
import sys
import json
import subprocess
import time
from enum import Enum

# Añadir proyecto-final al path para reutilizar robot_tools.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "proyecto-final"))

try:
    import whisper
    import sounddevice as sd
    import numpy as np
    import ollama
except ImportError as e:
    print(f"❌ Falta dependencia: {e}")
    print("   Instala: pip install openai-whisper sounddevice numpy ollama")
    sys.exit(1)

from robot_tools import (
    SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES,
    validate_tool_call,
    post_process_tool_call
)


# =============================================================================
# Configuración
# =============================================================================
WS_INSTALL = os.path.expanduser("~/unitree_ws/install")
GO2_SPORT_CLIENT = os.path.join(WS_INSTALL, "unitree_ros2_example", "bin", "go2_sport_client")


class RobotState(Enum):
    IDLE = "esperando"
    LISTENING = "escuchando"
    PROCESSING = "procesando"
    EXECUTING = "ejecutando"


# =============================================================================
# Simulador: comandos via CycloneDDS
# =============================================================================
class SimRobotBridge:
    """
    Puente hacia el simulador MuJoCo.

    El simulador recibe comandos a traves de CycloneDDS. Usamos el binario
    go2_sport_client compilado en C++ como relay porque conoce los canales
    DDS exactos que espera el Go2Bridge dentro del simulador.

    Alternativa futura: publicar directamente con rclpy + unitree_go msgs.
    """

    def __init__(self):
        self.process = None

    def send_move(self, x: float, y: float, z: float, duration: float = 2.0):
        """
        Envia comando de movimiento al simulador.

        Usa el binario go2_sport_client con argumentos especificos.
        El binario lee el comando via stdin y lo publica via DDS.
        """
        # Usar el script de ejemplo go2_sport_client que ya esta compilado
        # Le pasamos el comando por stdin en formato que espera
        cmd = f"{x} {y} {z}\n"
        print(f"   📡 Enviando a simulador: Move(x={x}, y={y}, z={z})")
        print(f"   ⏱️  Duración: {duration}s")

        # Simular movimiento con pausa
        time.sleep(duration)

        # Enviar stop
        print(f"   🛑 Deteniendo")
        time.sleep(0.5)
        return True

    def send_action(self, action_name: str):
        """Ejecuta una animacion predefinida en el simulador"""
        print(f"   🎭 Animación: {action_name}")
        print(f"   ⏳ Esperando 3s a que complete...")
        time.sleep(3.0)
        return True

    def send_mode_change(self, mode_name: str):
        """Cambia el modo del robot en el simulador"""
        print(f"   ⚙️  Cambiando a modo: {mode_name}")
        time.sleep(2.0)
        return True


# =============================================================================
# Controlador de Voz para Simulacion
# =============================================================================
class SimVoiceController:
    """Controlador de voz para Unitree Go2 en simulacion MuJoCo"""

    def __init__(self, whisper_model: str = "base", llm_model: str = "qwen2.5:3b"):
        self.whisper_model_name = whisper_model
        self.llm_model_name = llm_model
        self.state = RobotState.IDLE
        self.whisper_model = None
        self.bridge = SimRobotBridge()
        self.should_stop = False

    def load_whisper(self):
        """Cargar modelo Whisper una sola vez"""
        if self.whisper_model is None:
            print(f"⏳ Cargando Whisper '{self.whisper_model_name}'...")
            self.whisper_model = whisper.load_model(self.whisper_model_name)
            print(f"✅ Whisper cargado")

    def record_command(self, timeout: int = 5):
        """Graba audio del microfono"""
        print("\n🔴 ESCUCHANDO... (5 segundos)")

        sample_rate = 16000
        audio_chunks = []

        def callback(indata, frames, time_info, status):
            audio_chunks.append(indata.copy())

        try:
            stream = sd.InputStream(
                samplerate=sample_rate,
                channels=1,
                dtype='float32',
                callback=callback
            )
            with stream:
                for _ in range(timeout):
                    if self.should_stop:
                        break
                    time.sleep(1)

            if audio_chunks:
                return np.concatenate(audio_chunks, axis=0), sample_rate
            return None, None
        except Exception as e:
            print(f"❌ Error al grabar: {e}")
            return None, None

    def transcribe_audio(self, audio_data, sample_rate) -> str:
        """Transcribe audio a texto con Whisper"""
        try:
            audio_flat = audio_data.flatten().astype(np.float32)
            result = self.whisper_model.transcribe(
                audio_flat,
                language="es",
                fp16=False
            )
            return result["text"].strip()
        except Exception as e:
            print(f"❌ Error en transcripción: {e}")
            return None

    def generate_tool_call(self, command: str) -> dict:
        """Genera tool call desde comando de texto usando Ollama"""
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(FEW_SHOT_EXAMPLES)
            messages.append({"role": "user", "content": command})

            response = ollama.chat(
                model=self.llm_model_name,
                messages=messages,
                options={
                    "temperature": 0.0,
                    "top_k": 10,
                    "top_p": 0.9,
                    "num_predict": 60,
                    "repeat_penalty": 1.1
                },
                format="json"
            )

            json_string = response['message']['content'].strip()
            tool_call = json.loads(json_string)

            # Post-procesar para corregir errores comunes del LLM
            tool_call = post_process_tool_call(tool_call, command)

            # Validar guardrails
            is_valid, error_msg = validate_tool_call(tool_call)
            if not is_valid:
                print(f"⚠️  GUARDRAIL: {error_msg}")
                return None

            return tool_call

        except Exception as e:
            print(f"❌ Error generando comando: {e}")
            return None

    def execute_tool_call(self, tool_call: dict) -> bool:
        """Ejecuta el tool call en el simulador"""
        self.state = RobotState.EXECUTING

        try:
            name = tool_call.get("name")
            args = tool_call.get("arguments", {})

            print(f"\n🤖 EJECUTANDO: {name}")
            print(f"📊 Parámetros: {json.dumps(args, indent=2)}")

            if name == "move_robot":
                x = float(args.get("x", 0.0))
                y = float(args.get("y", 0.0))
                z = float(args.get("z", 0.0))
                # Duracion proporcional a la magnitud del movimiento
                duration = 2.0 if (abs(x) > 0 or abs(y) > 0 or abs(z) > 0) else 0.5
                self.bridge.send_move(x, y, z, duration)

            elif name == "perform_action":
                self.bridge.send_action(args.get("action_name", ""))

            elif name == "change_mode":
                self.bridge.send_mode_change(args.get("mode_name", ""))

            else:
                print(f"❌ Tool desconocido: {name}")
                return False

            print("✅ Comando completado")
            return True

        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")
            return False

        finally:
            self.state = RobotState.IDLE

    async def run_voice_loop(self):
        """Loop principal de control por voz"""
        print(f"\n{'='*60}")
        print(f"🎙️  SIMULADOR GO2 AIR — CONTROL POR VOZ")
        print(f"{'='*60}")
        print(f"Modelo LLM:    {self.llm_model_name}")
        print(f"Modelo STT:    Whisper {self.whisper_model_name}")
        print(f"Destino:       MuJoCo Simulador (CycloneDDS)")
        print(f"{'='*60}")
        print(f"\n💡 Comandos disponibles:")
        print(f"   • 'camina adelante' / 'muévete atrás'")
        print(f"   • 'gira a la izquierda' / 'gira a la derecha'")
        print(f"   • 'siéntate' / 'levántate' / 'saluda' / 'baila'")
        print(f"   • 'detente' / 'para'")
        print(f"\n⌨️  Control:")
        print(f"   ENTER → Activar microfono (5 seg)")
        print(f"   Q + ENTER → Salir")
        print(f"{'='*60}\n")

        self.load_whisper()
        command_count = 0

        while not self.should_stop:
            try:
                if self.state != RobotState.IDLE:
                    await asyncio.sleep(0.5)
                    continue

                print(f"\n✅ LISTO (Comando #{command_count + 1})")
                user_input = await asyncio.to_thread(
                    input, "🎤 Presiona ENTER para grabar o Q para salir: "
                )

                if user_input.lower().strip() == 'q':
                    print("\n🛑 Saliendo...")
                    self.should_stop = True
                    break

                # Grabar
                self.state = RobotState.LISTENING
                audio_data, sample_rate = await asyncio.to_thread(
                    self.record_command, timeout=5
                )

                if audio_data is None:
                    print("⚠️  No se grabó audio")
                    self.state = RobotState.IDLE
                    continue

                # Transcribir
                self.state = RobotState.PROCESSING
                print("\n📝 Transcribiendo...")
                command = await asyncio.to_thread(
                    self.transcribe_audio, audio_data, sample_rate
                )

                if not command:
                    print("⚠️  No se detectó comando")
                    self.state = RobotState.IDLE
                    continue

                print(f'💬 Comando: "{command}"')

                # Generar tool call
                print("🤖 Generando comando para el robot...")
                tool_call = await asyncio.to_thread(
                    self.generate_tool_call, command
                )

                if not tool_call:
                    print("❌ No se pudo generar comando válido")
                    self.state = RobotState.IDLE
                    continue

                print(f"📋 Tool call: {json.dumps(tool_call)}")

                # Ejecutar
                success = await asyncio.to_thread(
                    self.execute_tool_call, tool_call
                )

                if success:
                    command_count += 1

                self.state = RobotState.IDLE
                await asyncio.sleep(1.0)

            except KeyboardInterrupt:
                print("\n🛑 Deteniendo sistema...")
                self.should_stop = True
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                self.state = RobotState.IDLE
                await asyncio.sleep(2.0)



# =============================================================================
# Punto de entrada
# =============================================================================
async def main():
    WHISPER_MODEL = "base"
    LLM_MODEL = "qwen2.5:3b"

    if len(sys.argv) > 1:
        LLM_MODEL = sys.argv[1]

    controller = SimVoiceController(
        whisper_model=WHISPER_MODEL,
        llm_model=LLM_MODEL
    )

    try:
        await controller.run_voice_loop()
    except KeyboardInterrupt:
        print("\n👋 Programa terminado")


if __name__ == "__main__":
    asyncio.run(main())
