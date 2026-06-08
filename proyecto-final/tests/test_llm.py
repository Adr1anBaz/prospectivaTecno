#!/usr/bin/env python3
"""
Script de prueba para LLM local usando Ollama
"""

import ollama
import sys


def test_llm(model_name: str = "qwen2.5:0.5b", prompt: str = None):
    """
    Prueba el modelo LLM local

    Args:
        model_name: Nombre del modelo en Ollama
        prompt: Texto para enviar al modelo
    """
    print(f"🤖 Probando modelo: {model_name}")
    print("="*60)

    # Prompt por defecto si no se proporciona uno
    if not prompt:
        prompt = "¿Cuál es la capital de México?"
        print(f"💬 Prompt (por defecto): {prompt}")
    else:
        print(f"💬 Prompt: {prompt}")

    print("\n⏳ Generando respuesta...\n")

    try:
        # Llamar al modelo
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )

        # Mostrar respuesta
        print("="*60)
        print("🤖 RESPUESTA:")
        print("="*60)
        print(response['message']['content'])
        print("="*60)

        # Mostrar estadísticas
        if 'eval_count' in response:
            print(f"\n📊 Tokens generados: {response.get('eval_count', 'N/A')}")
            print(f"⏱️  Tiempo: {response.get('total_duration', 0) / 1e9:.2f}s")

        print("\n✅ Prueba completada")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Verifica que:")
        print("   1. Ollama esté corriendo: brew services start ollama")
        print(f"   2. El modelo esté instalado: ollama pull {model_name}")
        sys.exit(1)


def list_models():
    """Lista todos los modelos disponibles en Ollama"""
    print("📋 Modelos disponibles en Ollama:")
    print("="*60)

    try:
        models = ollama.list()
        if not models['models']:
            print("❌ No hay modelos instalados")
            print("\n💡 Instala un modelo con: ollama pull qwen2.5:0.5b")
            return

        for model in models['models']:
            name = model['name']
            size = model['size'] / (1024**3)  # Convertir a GB
            modified = model['modified_at']
            print(f"  • {name}")
            print(f"    Tamaño: {size:.2f} GB")
            print(f"    Modificado: {modified}")
            print()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Función principal"""
    # Verificar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_models()
            return
        elif sys.argv[1] == "--help":
            print("Uso:")
            print("  uv run python test_llm.py                    # Prueba con prompt por defecto")
            print("  uv run python test_llm.py 'tu pregunta'      # Prueba con tu prompt")
            print("  uv run python test_llm.py --list             # Lista modelos disponibles")
            return
        else:
            # El argumento es el prompt
            prompt = sys.argv[1]
            test_llm(prompt=prompt)
            return

    # Sin argumentos, usar prompt por defecto
    test_llm()


if __name__ == "__main__":
    main()
