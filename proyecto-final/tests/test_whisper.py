#!/usr/bin/env python3
"""
Script de prueba para Whisper local
Transcribe un archivo de audio usando el modelo Whisper
Solo muestra resultados en terminal, sin guardar archivos
"""

import whisper
import sys
import os


def test_whisper_model(audio_file: str = None, model_size: str = "base"):
    """
    Prueba el modelo Whisper con un archivo de audio

    Args:
        audio_file: Ruta al archivo de audio (mp3, wav, m4a, etc.)
        model_size: Tamaño del modelo (tiny, base, small, medium, large)
    """
    print(f"🔄 Cargando modelo Whisper '{model_size}'...")

    try:
        # Cargar el modelo
        model = whisper.load_model(model_size)
        print(f"✅ Modelo '{model_size}' cargado exitosamente")

        # Si no se proporciona archivo, solo verificar que el modelo carga
        if not audio_file:
            print("\n✅ Whisper está funcionando correctamente")
            print(f"📝 Modelo cargado: {model_size}")
            print("\n💡 Este script solo muestra resultados en terminal")
            print("   No guarda archivos de transcripción")
            print("\nPara transcribir un archivo, ejecuta:")
            print(f"  uv run python test_whisper.py <ruta_al_audio>")
            print("\nEjemplo:")
            print(f"  uv run python test_whisper.py audio.mp3")
            print("\nPara grabar y guardar transcripciones:")
            print(f"  uv run python record_and_transcribe.py")
            return

        # Verificar que existe el archivo
        if not os.path.exists(audio_file):
            print(f"❌ Error: El archivo '{audio_file}' no existe")
            return

        print(f"\n🎵 Transcribiendo: {audio_file}")
        print("⏳ Esto puede tomar unos momentos...")

        # Transcribir
        result = model.transcribe(audio_file, language="es", fp16=False)

        # Mostrar resultados solo en terminal
        print("\n" + "="*60)
        print("📝 TRANSCRIPCIÓN:")
        print("="*60)
        print(result["text"])
        print("="*60)

        print("\n✅ Proceso completado")
        print("💡 Transcripción mostrada en terminal (no se guardó archivo)")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Obtener archivo de audio desde argumentos
    audio_file = sys.argv[1] if len(sys.argv) > 1 else None

    # Puedes cambiar el tamaño del modelo aquí
    # Opciones: tiny, base, small, medium, large
    MODEL_SIZE = "base"  # Buen balance entre velocidad y precisión

    test_whisper_model(audio_file, MODEL_SIZE)
