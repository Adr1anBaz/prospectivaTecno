#!/usr/bin/env python3
"""
Sistema de control continuo de robot Unitree por comandos de voz
Loop infinito: Escucha → Transcribe → Genera comando → Ejecuta
"""

import asyncio
import os
import sys
import whisper
import sounddevice as sd
import numpy as np
import ollama
import json
from enum import Enum
from datetime import datetime
from unitree_webrtc_connect.webrtc_driver import UnitreeWebRTCConnection, WebRTCConnectionMethod
from unitree_webrtc_connect.constants import RTC_TOPIC, SPORT_CMD

from robot_tools import (
    SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES,
    validate_tool_call,
    post_process_tool_call
)


class RobotState(Enum):
    """Estados del robot"""
    DISCONNECTED = "desconectado"
    IDLE = "esperando"
    LISTENING = "escuchando"
    PROCESSING = "procesando"
    EXECUTING = "ejecutando"


class UnitreeVoiceController:
    """Controlador de voz para robot Unitree"""

    def __init__(self, robot_ip: str = None, whisper_model: str = "base", llm_model: str = "qwen2.5:3b"):
        self.robot_ip = robot_ip or os.environ.get("UNITREE_ROBOT_IP", "192.168.12.1")
        self.whisper_model_name = whisper_model
        self.llm_model_name = llm_model

        self.state = RobotState.DISCONNECTED
        self.conn = None
        self.whisper_model = None

        # Control de ejecución
        self.is_executing = False
        self.should_stop = False

    async def connect_robot(self):
        """Conectar al robot via WebRTC"""
        print(f"\n{'='*60}")
        print(f"🤖 CONECTANDO AL ROBOT UNITREE")
        print(f"{'='*60}")
        print(f"📡 IP: {self.robot_ip}")

        try:
            self.conn = UnitreeWebRTCConnection(
                WebRTCConnectionMethod.LocalAP,
                ip=self.robot_ip
            )
            await self.conn.connect()

            print(f"✅ Conexión WebRTC establecida")
            self.state = RobotState.IDLE
            return True

        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            return False

    def load_whisper(self):
        """Cargar modelo Whisper"""
        if self.whisper_model is None:
            print(f"\n⏳ Cargando Whisper '{self.whisper_model_name}'...")
            self.whisper_model = whisper.load_model(self.whisper_model_name)
            print(f"✅ Whisper cargado")

    def record_command(self) -> tuple:
        """
        Graba un comando de voz - el usuario controla inicio y fin

        Returns:
            (audio_data, sample_rate) o (None, None) si falla
        """
        print("\n⏺️  🔴 GRABANDO... (presiona ENTER para DETENER)")

        sample_rate = 16000
        audio_chunks = []
        recording = True

        def callback(indata, frames, time, status):
            if recording and not self.should_stop:
                audio_chunks.append(indata.copy())

        try:
            stream = sd.InputStream(
                samplerate=sample_rate,
                channels=1,
                dtype='float32',
                callback=callback
            )

            with stream:
                # Esperar a que el usuario presione ENTER para detener
                input()

            recording = False

            if audio_chunks:
                audio_data = np.concatenate(audio_chunks, axis=0)
                duration = len(audio_data) / sample_rate
                print(f"⏹️  Grabación detenida ({duration:.1f} segundos)")
                return audio_data, sample_rate
            else:
                return None, None

        except KeyboardInterrupt:
            print(f"\n⚠️  Grabación cancelada")
            return None, None
        except Exception as e:
            print(f"❌ Error al grabar: {e}")
            return None, None

    def transcribe_audio(self, audio_data, sample_rate) -> str:
        """Transcribe audio a texto"""
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
        """Genera tool call desde comando de texto"""
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

            # Post-procesar
            tool_call = post_process_tool_call(tool_call, command)

            # Validar
            is_valid, error_msg = validate_tool_call(tool_call)
            if not is_valid:
                print(f"⚠️  GUARDRAIL: {error_msg}")
                return None

            return tool_call

        except Exception as e:
            print(f"❌ Error generando comando: {e}")
            return None

    async def execute_tool_call(self, tool_call: dict) -> bool:
        """Ejecuta el tool call en el robot real"""
        if self.is_executing:
            print("⚠️  Ya hay un comando ejecutándose, ignorando...")
            return False

        self.is_executing = True
        self.state = RobotState.EXECUTING

        try:
            name = tool_call.get("name")
            args = tool_call.get("arguments", {})

            print(f"\n🤖 EJECUTANDO: {name}")
            print(f"📊 Parámetros: {json.dumps(args, indent=2)}")

            if name == "move_robot":
                await self.execute_move(args.get("x", 0.0), args.get("y", 0.0), args.get("z", 0.0))

            elif name == "perform_action":
                await self.execute_action(args.get("action_name"))

            elif name == "change_mode":
                await self.execute_mode_change(args.get("mode_name"))

            else:
                print(f"❌ Tool desconocido: {name}")
                return False

            print("✅ Comando completado")
            return True

        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")
            return False

        finally:
            self.is_executing = False
            self.state = RobotState.IDLE

    async def execute_move(self, x: float, y: float, z: float):
        """Ejecuta movimiento del robot"""
        # Duración basada en magnitud del comando
        duration = 2.0 if (abs(x) > 0 or abs(y) > 0) else 0.5

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {"x": float(x), "y": float(y), "z": float(z)}
            }
        )

        await asyncio.sleep(duration)

        # Detener después de la duración
        if abs(x) > 0 or abs(y) > 0 or abs(z) > 0:
            await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"],
                {
                    "api_id": SPORT_CMD["Move"],
                    "parameter": {"x": 0.0, "y": 0.0, "z": 0.0}
                }
            )
            await asyncio.sleep(0.5)

    async def execute_action(self, action_name: str):
        """Ejecuta animación del robot"""
        # Mapear nombre a comando
        cmd_map = {
            "StandUp": SPORT_CMD["StandUp"],
            "Sit": SPORT_CMD["Sit"],
            "StandDown": SPORT_CMD["StandDown"],
            "Hello": SPORT_CMD["Hello"],
            "Stretch": SPORT_CMD["Stretch"],
            "Dance1": SPORT_CMD["Dance1"],
            "RecoveryStand": SPORT_CMD["RecoveryStand"]
        }

        cmd_id = cmd_map.get(action_name)
        if not cmd_id:
            print(f"❌ Animación desconocida: {action_name}")
            return

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {"api_id": cmd_id}
        )

        # Esperar a que complete la animación
        await asyncio.sleep(3.0)

    async def execute_mode_change(self, mode_name: str):
        """Cambia el modo del robot"""
        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["MOTION_SWITCHER"],
            {"api_id": 1002, "parameter": {"name": mode_name.lower()}}
        )

        # Esperar a que el modo cambie
        await asyncio.sleep(3.0)

    async def run_voice_loop(self):
        """Loop principal de escucha con control manual"""
        print(f"\n{'='*60}")
        print(f"🎙️  SISTEMA DE CONTROL POR VOZ ACTIVO")
        print(f"{'='*60}")
        print(f"Modelo LLM: {self.llm_model_name}")
        print(f"Modelo Whisper: {self.whisper_model_name}")
        print(f"\n💡 Comandos de voz disponibles:")
        print(f"   • Movimiento: 'camina adelante', 'gira a la derecha'")
        print(f"   • Animaciones: 'siéntate', 'saluda', 'baila'")
        print(f"   • Modos: 'modo normal', 'apaga motores'")
        print(f"   • Control: 'detente', 'para'")
        print(f"\n⌨️  Control del sistema:")
        print(f"   • ENTER → Activar micrófono (inicio de grabación)")
        print(f"   • ENTER nuevamente → Detener grabación")
        print(f"   • Q + ENTER → Salir de forma segura")
        print(f"{'='*60}\n")

        # Cargar Whisper una sola vez
        self.load_whisper()

        command_count = 0

        while not self.should_stop:
            try:
                # Verificar estado
                if self.state != RobotState.IDLE:
                    await asyncio.sleep(0.5)
                    continue

                # Indicar que está listo y esperar input
                print(f"\n{'='*60}")
                print(f"✅ LISTO (Comando #{command_count + 1})")
                print(f"{'='*60}")
                print(f"🎤 Presiona ENTER para grabar o Q para salir: ", end='', flush=True)

                # Esperar input del usuario (en thread para no bloquear)
                user_input = await asyncio.to_thread(input)

                # Procesar input
                if user_input.lower().strip() == 'q':
                    print("\n🛑 Saliendo de forma segura...")
                    self.should_stop = True
                    break

                # Si presionó ENTER (o cualquier otra tecla), grabar
                print("\n🎙️  Micrófono ACTIVADO")

                # Cambiar estado
                self.state = RobotState.LISTENING

                # Grabar comando (usuario controla duración)
                audio_data, sample_rate = await asyncio.to_thread(
                    self.record_command
                )

                if audio_data is None:
                    print("⚠️  No se grabó audio, reintentando...")
                    self.state = RobotState.IDLE
                    continue

                # Transcribir
                self.state = RobotState.PROCESSING
                print("\n📝 Transcribiendo...")

                command = await asyncio.to_thread(
                    self.transcribe_audio,
                    audio_data,
                    sample_rate
                )

                if not command:
                    print("⚠️  No se detectó comando, reintentando...")
                    self.state = RobotState.IDLE
                    continue

                print(f"💬 Comando: \"{command}\"")

                # Generar tool call
                print("🤖 Generando comando para el robot...")

                tool_call = await asyncio.to_thread(
                    self.generate_tool_call,
                    command
                )

                if not tool_call:
                    print("❌ No se pudo generar comando válido")
                    self.state = RobotState.IDLE
                    continue

                print(f"📋 Tool call: {json.dumps(tool_call)}")

                # Ejecutar
                success = await self.execute_tool_call(tool_call)

                if success:
                    command_count += 1

                # Volver a estado idle
                self.state = RobotState.IDLE

                # Pequeña pausa antes del siguiente ciclo
                await asyncio.sleep(1.0)

            except KeyboardInterrupt:
                print("\n\n🛑 Deteniendo sistema...")
                self.should_stop = True
                break

            except Exception as e:
                print(f"\n❌ Error en loop: {e}")
                import traceback
                traceback.print_exc()
                self.state = RobotState.IDLE
                await asyncio.sleep(2.0)

    async def shutdown(self):
        """Cierra conexiones y limpia recursos"""
        print("\n🔌 Cerrando conexión con el robot...")

        if self.conn:
            # Detener movimiento antes de desconectar
            if self.state == RobotState.EXECUTING:
                try:
                    await self.conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["SPORT_MOD"],
                        {
                            "api_id": SPORT_CMD["Move"],
                            "parameter": {"x": 0.0, "y": 0.0, "z": 0.0}
                        }
                    )
                    await asyncio.sleep(0.5)
                except:
                    pass

            await self.conn.disconnect()

        print("✅ Sistema cerrado correctamente")


async def main():
    """Función principal"""
    # Configuración
    ROBOT_IP = os.environ.get("UNITREE_ROBOT_IP", "192.168.12.1")
    WHISPER_MODEL = "base"
    LLM_MODEL = "qwen2.5:3b"

    # Crear controlador
    controller = UnitreeVoiceController(
        robot_ip=ROBOT_IP,
        whisper_model=WHISPER_MODEL,
        llm_model=LLM_MODEL
    )

    try:
        # Conectar al robot
        if not await controller.connect_robot():
            print("❌ No se pudo conectar al robot")
            return

        # Iniciar loop de voz
        await controller.run_voice_loop()

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupción detectada")

    finally:
        await controller.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Programa terminado")
