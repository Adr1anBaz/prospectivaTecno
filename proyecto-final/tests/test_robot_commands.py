#!/usr/bin/env python3
"""
Script de testing automatizado para validar comandos del robot
Prueba todos los casos sin necesidad de voz
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para importar robot_tools
sys.path.insert(0, str(Path(__file__).parent.parent))

import ollama
import json
from robot_tools import (
    SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES,
    validate_tool_call,
    post_process_tool_call
)

# ==========================================
# CASOS DE PRUEBA
# ==========================================
TEST_CASES = [
    # Animaciones básicas
    {
        "command": "haz que el perro salude",
        "expected_tool": "perform_action",
        "expected_args": {"action_name": "Hello"},
        "category": "Animaciones"
    },
    {
        "command": "siéntate",
        "expected_tool": "perform_action",
        "expected_args": {"action_name": "Sit"},
        "category": "Animaciones"
    },
    {
        "command": "ponte de pie",
        "expected_tool": "perform_action",
        "expected_args": {"action_name": "StandUp"},
        "category": "Animaciones"
    },
    {
        "command": "estírate",
        "expected_tool": "perform_action",
        "expected_args": {"action_name": "Stretch"},
        "category": "Animaciones"
    },
    {
        "command": "baila",
        "expected_tool": "perform_action",
        "expected_args": {"action_name": "Dance1"},
        "category": "Animaciones"
    },

    # Movimientos adelante/atrás
    {
        "command": "camina hacia adelante",
        "expected_tool": "move_robot",
        "expected_args": {"x": ">0", "y": "0", "z": "0"},
        "category": "Movimiento frontal"
    },
    {
        "command": "muévete hacia atrás",
        "expected_tool": "move_robot",
        "expected_args": {"x": "<0", "y": "0", "z": "0"},
        "category": "Movimiento frontal"
    },

    # Movimientos laterales (CRÍTICO)
    {
        "command": "muévete a la izquierda",
        "expected_tool": "move_robot",
        "expected_args": {"x": "0", "y": ">0", "z": "0"},
        "category": "Movimiento lateral"
    },
    {
        "command": "muévete a la derecha",
        "expected_tool": "move_robot",
        "expected_args": {"x": "0", "y": "<0", "z": "0"},
        "category": "Movimiento lateral"
    },

    # Giros (CRÍTICO)
    {
        "command": "gira a la izquierda",
        "expected_tool": "move_robot",
        "expected_args": {"x": "0", "y": "0", "z": ">0"},
        "category": "Giros"
    },
    {
        "command": "gira a la derecha",
        "expected_tool": "move_robot",
        "expected_args": {"x": "0", "y": "0", "z": "<0"},
        "category": "Giros"
    },

    # Detener (CRÍTICO)
    {
        "command": "detente",
        "expected_tool": "move_robot",
        "expected_args": {"x": "0", "y": "0", "z": "0"},
        "category": "Control"
    },
    {
        "command": "para",
        "expected_tool": "move_robot",
        "expected_args": {"x": "0", "y": "0", "z": "0"},
        "category": "Control"
    },

    # Movimientos compuestos
    {
        "command": "retrocede girando a la izquierda",
        "expected_tool": "move_robot",
        "expected_args": {"x": "<0", "y": "0", "z": ">0"},
        "category": "Movimientos compuestos"
    },
    {
        "command": "avanza girando a la derecha",
        "expected_tool": "move_robot",
        "expected_args": {"x": ">0", "y": "0", "z": "<0"},
        "category": "Movimientos compuestos"
    },

    # Cambios de modo (CRÍTICO: mcf)
    {
        "command": "activa el modo caminar",
        "expected_tool": "change_mode",
        "expected_args": {"mode_name": "normal"},
        "category": "Modos"
    },
    {
        "command": "activa el modo de acrobacias",
        "expected_tool": "change_mode",
        "expected_args": {"mode_name": "ai"},
        "category": "Modos"
    },
    {
        "command": "apaga los motores",
        "expected_tool": "change_mode",
        "expected_args": {"mode_name": "mcf"},
        "category": "Modos"
    },
    {
        "command": "modo seguro",
        "expected_tool": "change_mode",
        "expected_args": {"mode_name": "mcf"},
        "category": "Modos"
    },
]


def generate_tool_call(command: str, model_name: str = "qwen2.5:3b", verbose: bool = False):
    """Genera tool call para un comando de texto"""
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(FEW_SHOT_EXAMPLES)
        messages.append({"role": "user", "content": command})

        response = ollama.chat(
            model=model_name,
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

        if verbose:
            print(f"JSON: {json_string}")

        return tool_call, None

    except json.JSONDecodeError as e:
        return None, f"JSON inválido: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"


def check_expected(actual_args: dict, expected_args: dict) -> tuple[bool, str]:
    """Compara argumentos actuales con esperados"""
    issues = []

    for key, expected_val in expected_args.items():
        actual_val = actual_args.get(key)

        if expected_val == ">0":
            if actual_val is None or float(actual_val) <= 0:
                issues.append(f"{key} debería ser >0, obtuvo {actual_val}")
        elif expected_val == "<0":
            if actual_val is None or float(actual_val) >= 0:
                issues.append(f"{key} debería ser <0, obtuvo {actual_val}")
        elif expected_val == "0":
            if actual_val is None or float(actual_val) != 0.0:
                issues.append(f"{key} debería ser 0, obtuvo {actual_val}")
        else:
            # Comparación exacta para strings
            if actual_val != expected_val:
                issues.append(f"{key} debería ser '{expected_val}', obtuvo '{actual_val}'")

    if issues:
        return False, "; ".join(issues)
    return True, "OK"


def run_tests(model_name: str = "qwen2.5:3b"):
    """Ejecuta todos los tests y genera reporte"""
    print("="*80)
    print(f"🧪 TEST SUITE - ROBOT COMMAND VALIDATION")
    print(f"🤖 Modelo: {model_name}")
    print("="*80)

    results = {
        "passed": [],
        "failed": [],
        "errors": []
    }

    for i, test in enumerate(TEST_CASES, 1):
        command = test["command"]
        expected_tool = test["expected_tool"]
        expected_args = test["expected_args"]
        category = test["category"]

        print(f"\n[{i}/{len(TEST_CASES)}] Testing: \"{command}\"")
        print(f"    Categoría: {category}")

        # Generar tool call
        tool_call_raw, error = generate_tool_call(command, model_name)

        if error:
            print(f"    ❌ ERROR: {error}")
            results["errors"].append({
                "command": command,
                "category": category,
                "error": error
            })
            continue

        # Post-procesar para corregir errores comunes
        tool_call = post_process_tool_call(tool_call_raw, command)

        # Validar guardrails
        is_valid, validation_msg = validate_tool_call(tool_call)
        if not is_valid:
            print(f"    ❌ GUARDRAIL BLOQUEADO: {validation_msg}")
            results["failed"].append({
                "command": command,
                "category": category,
                "reason": f"Guardrail: {validation_msg}",
                "tool_call": tool_call
            })
            continue

        # Verificar tool correcto
        actual_tool = tool_call.get("name")
        if actual_tool != expected_tool:
            print(f"    ❌ TOOL INCORRECTO: esperaba '{expected_tool}', obtuvo '{actual_tool}'")
            results["failed"].append({
                "command": command,
                "category": category,
                "reason": f"Tool incorrecto: {actual_tool} != {expected_tool}",
                "tool_call": tool_call
            })
            continue

        # Verificar argumentos
        actual_args = tool_call.get("arguments", {})
        args_ok, args_msg = check_expected(actual_args, expected_args)

        if not args_ok:
            print(f"    ❌ ARGUMENTOS INCORRECTOS: {args_msg}")
            print(f"       Obtuvo: {json.dumps(actual_args)}")
            results["failed"].append({
                "command": command,
                "category": category,
                "reason": args_msg,
                "tool_call": tool_call
            })
            continue

        # Test pasado
        print(f"    ✅ PASS - {json.dumps(tool_call)}")
        results["passed"].append({
            "command": command,
            "category": category,
            "tool_call": tool_call
        })

    # Reporte final
    print("\n" + "="*80)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*80)

    total = len(TEST_CASES)
    passed = len(results["passed"])
    failed = len(results["failed"])
    errors = len(results["errors"])

    print(f"\n✅ Pasados: {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"❌ Fallados: {failed}/{total} ({failed/total*100:.1f}%)")
    print(f"⚠️  Errores: {errors}/{total}")

    # Desglose por categoría
    if results["failed"]:
        print("\n" + "="*80)
        print("❌ TESTS FALLIDOS:")
        print("="*80)

        by_category = {}
        for fail in results["failed"]:
            cat = fail["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(fail)

        for category, fails in by_category.items():
            print(f"\n📂 {category}:")
            for fail in fails:
                print(f"   • \"{fail['command']}\"")
                print(f"     Razón: {fail['reason']}")
                print(f"     Tool call: {json.dumps(fail['tool_call'])}")

    if results["errors"]:
        print("\n" + "="*80)
        print("⚠️  ERRORES:")
        print("="*80)
        for error in results["errors"]:
            print(f"   • \"{error['command']}\": {error['error']}")

    print("\n" + "="*80)

    # Veredicto final
    if passed == total:
        print("🎉 TODOS LOS TESTS PASARON - Modelo funcionando correctamente")
    elif passed / total >= 0.8:
        print("⚠️  MODELO FUNCIONAL pero con algunos fallos")
    else:
        print("❌ MODELO NECESITA MEJORAS - Muchos tests fallaron")

    print("="*80)

    return results


def compare_models(models: list):
    """Compara múltiples modelos y determina el mejor"""
    print("="*80)
    print("🏆 COMPARACIÓN DE MODELOS")
    print("="*80)

    all_results = {}

    for model in models:
        print(f"\n{'='*80}")
        print(f"Testing modelo: {model}")
        print(f"{'='*80}")

        results = run_tests(model)
        all_results[model] = results

        # Pequeña pausa entre modelos
        import time
        time.sleep(1)

    # Tabla comparativa
    print("\n" + "="*80)
    print("📊 TABLA COMPARATIVA")
    print("="*80)
    print(f"\n{'Modelo':<20} {'Pasados':<12} {'Fallados':<12} {'Errores':<12} {'% Éxito':<10}")
    print("-"*80)

    best_model = None
    best_score = 0

    for model, results in all_results.items():
        total = len(TEST_CASES)
        passed = len(results["passed"])
        failed = len(results["failed"])
        errors = len(results["errors"])
        success_rate = passed / total * 100

        print(f"{model:<20} {passed:<12} {failed:<12} {errors:<12} {success_rate:<10.1f}%")

        if success_rate > best_score:
            best_score = success_rate
            best_model = model

    print("-"*80)
    print(f"\n🏆 MEJOR MODELO: {best_model} ({best_score:.1f}% éxito)")

    # Detalles de fallos por modelo
    print("\n" + "="*80)
    print("🔍 ANÁLISIS DE FALLOS POR MODELO")
    print("="*80)

    for model, results in all_results.items():
        if results["failed"]:
            print(f"\n❌ {model}:")
            for fail in results["failed"]:
                print(f"   • {fail['command']}: {fail['reason']}")
        else:
            print(f"\n✅ {model}: Sin fallos")

    return all_results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--compare":
        # Modo comparación
        models_to_test = [
            "qwen2.5:3b",
            "qwen2.5:1.5b",
            "llama3.2:1b",
        ]

        # Verificar si llama3.2:3b está disponible
        try:
            import subprocess
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if "llama3.2:3b" in result.stdout:
                models_to_test.append("llama3.2:3b")
        except:
            pass

        compare_models(models_to_test)
    else:
        # Modo individual
        model = "qwen2.5:3b"
        if len(sys.argv) > 1:
            model = sys.argv[1]

        results = run_tests(model)
