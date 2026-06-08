#!/usr/bin/env python3
"""
Script para ejecutar múltiples modelos de Ollama con el mismo prompt.
Útil para comparar respuestas de diferentes modelos.
"""

import ollama
import time
from datetime import datetime

# Lista de modelos a probar
MODELOS = [
    "llama3.2:3b",
    "gemma2:2b",
    "qwen2.5:7b",
    "mistral:7b",
    "phi4",
    "tinyllama",
]

# Prompt que se usará para todos los modelos
PROMPT = "¿Qué es la inteligencia artificial y cuáles son sus aplicaciones principales en español?"


def ejecutar_modelo(modelo: str, prompt: str) -> dict:
    """
    Ejecuta un modelo con un prompt y retorna la respuesta con metadatos.

    Args:
        modelo: Nombre del modelo en Ollama (ej: "llama3.2:3b")
        prompt: Texto del prompt a enviar

    Returns:
        Dict con respuesta, tiempo de ejecución, y metadatos
    """
    print(f"\n{'='*80}")
    print(f"🤖 Modelo: {modelo}")
    print(f"{'='*80}")

    inicio = time.time()

    try:
        response = ollama.chat(
            model=modelo,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        tiempo_ejecucion = time.time() - inicio
        respuesta_texto = response['message']['content']

        print(f"\n📝 Respuesta:\n{respuesta_texto}")
        print(f"\n⏱️  Tiempo: {tiempo_ejecucion:.2f} segundos")

        return {
            'modelo': modelo,
            'respuesta': respuesta_texto,
            'tiempo': tiempo_ejecucion,
            'exito': True,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ Error ejecutando {modelo}: {str(e)}")
        return {
            'modelo': modelo,
            'error': str(e),
            'exito': False,
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Ejecuta todos los modelos y recopila resultados."""
    print("🚀 Iniciando ejecución de modelos")
    print(f"📋 Prompt: \"{PROMPT}\"")
    print(f"🔢 Modelos a ejecutar: {len(MODELOS)}")

    resultados = []

    for modelo in MODELOS:
        resultado = ejecutar_modelo(modelo, PROMPT)
        resultados.append(resultado)

        # Pequeña pausa entre modelos
        time.sleep(1)

    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("="*80)

    exitosos = [r for r in resultados if r.get('exito')]
    fallidos = [r for r in resultados if not r.get('exito')]

    print(f"\n✅ Exitosos: {len(exitosos)}/{len(MODELOS)}")
    print(f"❌ Fallidos: {len(fallidos)}/{len(MODELOS)}")

    if exitosos:
        print("\n⏱️  Tiempos de ejecución:")
        for r in sorted(exitosos, key=lambda x: x['tiempo']):
            print(f"  • {r['modelo']}: {r['tiempo']:.2f}s")

    if fallidos:
        print("\n❌ Modelos con errores:")
        for r in fallidos:
            print(f"  • {r['modelo']}: {r.get('error', 'Error desconocido')}")

    print("\n" + "="*80)
    print("✨ ¡Ejecución completada!")
    print("\nRecomendaciones:")
    print("  1. Toma captura de pantalla de cada ejecución")
    print("  2. Guarda las capturas en la carpeta 'ejecuciones/'")
    print("  3. Compara las respuestas en tu tabla comparativa")
    print("="*80)


if __name__ == "__main__":
    main()
