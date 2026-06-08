#!/usr/bin/env python3
"""
Script para obtener información detallada de los modelos instalados en Ollama.
"""

import ollama
import json


def mostrar_info_modelo(modelo: str):
    """
    Muestra información detallada de un modelo.

    Args:
        modelo: Nombre del modelo (ej: "llama3.2:3b")
    """
    print(f"\n{'='*80}")
    print(f"🤖 Modelo: {modelo}")
    print(f"{'='*80}")

    try:
        info = ollama.show(modelo)

        # Información básica
        print(f"\n📋 Información General:")
        if 'modelfile' in info:
            lines = info['modelfile'].split('\n')
            for line in lines[:10]:  # Primeras 10 líneas
                if line.strip():
                    print(f"  {line}")

        # Template
        if 'template' in info:
            print(f"\n💬 Template:")
            print(f"  {info['template'][:200]}...")  # Primeros 200 caracteres

        # Parámetros
        if 'parameters' in info:
            print(f"\n⚙️  Parámetros:")
            print(f"  {info['parameters']}")

        # Details
        if 'details' in info:
            details = info['details']
            print(f"\n📊 Detalles:")
            print(f"  • Formato: {details.get('format', 'N/A')}")
            print(f"  • Familia: {details.get('family', 'N/A')}")
            print(f"  • Parámetros: {details.get('parameter_size', 'N/A')}")
            print(f"  • Cuantización: {details.get('quantization_level', 'N/A')}")

    except Exception as e:
        print(f"❌ Error obteniendo info de {modelo}: {str(e)}")


def listar_modelos():
    """Lista todos los modelos instalados."""
    print("\n" + "="*80)
    print("📦 MODELOS INSTALADOS")
    print("="*80)

    try:
        modelos = ollama.list()

        if not modelos.get('models'):
            print("\n⚠️  No hay modelos instalados")
            return []

        print(f"\n🔢 Total: {len(modelos['models'])} modelos\n")

        nombres = []
        for modelo in modelos['models']:
            nombre = modelo['name']
            size = modelo.get('size', 0)
            size_gb = size / (1024**3)
            modified = modelo.get('modified_at', 'N/A')

            print(f"  • {nombre}")
            print(f"    ├─ Tamaño: {size_gb:.2f} GB")
            print(f"    └─ Modificado: {modified}")
            print()

            nombres.append(nombre)

        return nombres

    except Exception as e:
        print(f"❌ Error listando modelos: {str(e)}")
        return []


def main():
    """Función principal."""
    import sys

    if len(sys.argv) > 1:
        # Mostrar info de modelo específico
        modelo = sys.argv[1]
        mostrar_info_modelo(modelo)
    else:
        # Listar todos y mostrar info de cada uno
        modelos = listar_modelos()

        if modelos:
            print("\n" + "="*80)
            respuesta = input("\n¿Deseas ver información detallada de cada modelo? (s/n): ")

            if respuesta.lower() == 's':
                for modelo in modelos:
                    mostrar_info_modelo(modelo)
                    input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    main()
