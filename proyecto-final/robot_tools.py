"""
Definición de tools y guardrails para control de robot Unitree
Optimizado para modelos LLM pequeños (<1B parámetros)
"""

import re

# ==========================================
# GUARDRAILS (REGEX & LIMITS)
# ==========================================
GUARDRAILS = {
    # Solo permite números flotantes entre -0.5 y 0.5
    "safe_speed": re.compile(r"^-?0\.[0-5]$|^0\.0$"),
    # Solo permite flotantes entre -1.0 y 1.0 para giros
    "safe_rotation": re.compile(r"^-?(?:0\.[0-9]|1\.0)$|^0\.0$"),
    # Lista blanca de acciones físicas
    "allowed_actions": re.compile(
        r"^(StandUp|Sit|StandDown|Hello|Stretch|Dance1|RecoveryStand)$",
        re.IGNORECASE
    ),
    # Lista blanca de modos de sistema
    "allowed_modes": re.compile(r"^(normal|ai|mcf)$", re.IGNORECASE)
}

# ==========================================
# TOOLS SCHEMA (Formato simplificado)
# ==========================================
ROBOT_TOOLS = [
    {
        "name": "move_robot",
        "description": "Mueve el robot. x=adelante/atrás, y=lateral, z=giro",
        "parameters": {
            "x": "float (-0.5 a 0.5) velocidad frontal",
            "y": "float (-0.5 a 0.5) velocidad lateral",
            "z": "float (-1.0 a 1.0) velocidad de giro"
        }
    },
    {
        "name": "perform_action",
        "description": "Ejecuta una animación predefinida",
        "parameters": {
            "action_name": "string (StandUp|Sit|StandDown|Hello|Stretch|Dance1|RecoveryStand)"
        }
    },
    {
        "name": "change_mode",
        "description": "Cambia el modo del robot",
        "parameters": {
            "mode_name": "string (normal|ai|mcf)"
        }
    }
]

# ==========================================
# SYSTEM PROMPT (Optimizado para <1B)
# ==========================================
SYSTEM_PROMPT = """Eres el procesador de comandos de un robot cuadrúpedo.
Tu ÚNICA función es mapear la orden del usuario a un JSON estricto.
PROHIBIDO generar texto conversacional, saludos o explicaciones. SOLO debes imprimir JSON válido.

### HERRAMIENTAS DISPONIBLES ###
1. Moverse
   - JSON: {"name": "move_robot", "arguments": {"x": [float], "y": [float], "z": [float]}}
   - x: adelante(+) / atrás(-), rango -0.5 a 0.5
   - y: izquierda(+) / derecha(-), rango -0.5 a 0.5
   - z: girar izquierda(+) / girar derecha(-), rango -1.0 a 1.0

2. Animaciones
   - JSON: {"name": "perform_action", "arguments": {"action_name": "[string]"}}
   - Opciones: "StandUp", "Sit", "StandDown", "Hello", "Stretch", "Dance1", "RecoveryStand"

3. Cambiar Estado
   - JSON: {"name": "change_mode", "arguments": {"mode_name": "[string]"}}
   - "normal" = modo caminar
   - "ai" = modo acrobacias
   - "mcf" = apagar motores / modo seguro

### REGLAS CRÍTICAS ###
- "detente" o "para" = {"x": 0.0, "y": 0.0, "z": 0.0}
- "izquierda" = y positivo (+) o z positivo (+) según contexto
- "derecha" = y negativo (-) o z negativo (-) según contexto
- "apagar" o "seguro" = mode "mcf"

### FORMATO DE RESPUESTA ###
Debes responder con un único objeto JSON. Nada más."""

# ==========================================
# FEW-SHOT EXAMPLES
# ==========================================
FEW_SHOT_EXAMPLES = [
    # Animaciones
    {
        "role": "user",
        "content": "haz que el perro salude"
    },
    {
        "role": "assistant",
        "content": '{"name": "perform_action", "arguments": {"action_name": "Hello"}}'
    },
    {
        "role": "user",
        "content": "siéntate"
    },
    {
        "role": "assistant",
        "content": '{"name": "perform_action", "arguments": {"action_name": "Sit"}}'
    },
    {
        "role": "user",
        "content": "ponte de pie"
    },
    {
        "role": "assistant",
        "content": '{"name": "perform_action", "arguments": {"action_name": "StandUp"}}'
    },
    # Movimientos adelante/atrás
    {
        "role": "user",
        "content": "camina hacia adelante"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.3, "y": 0.0, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "muévete hacia atrás"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": -0.3, "y": 0.0, "z": 0.0}}'
    },
    # Movimientos laterales (CRÍTICO: izquierda = y+, derecha = y-)
    # MUCHOS ejemplos porque el modelo se confunde
    {
        "role": "user",
        "content": "muévete a la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.3, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "camina a la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.3, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "ve hacia la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.2, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "desplázate a la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.3, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "ve a la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.3, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "muévete a la derecha"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": -0.3, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "camina a la derecha"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": -0.3, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "ve hacia la derecha"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": -0.2, "z": 0.0}}'
    },
    # Giros (CRÍTICO: izquierda = z+, derecha = z-)
    {
        "role": "user",
        "content": "gira a la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.0, "z": 0.5}}'
    },
    {
        "role": "user",
        "content": "rota a la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.0, "z": 0.4}}'
    },
    {
        "role": "user",
        "content": "voltea a la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.0, "z": 0.5}}'
    },
    {
        "role": "user",
        "content": "gira a la derecha"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.0, "z": -0.5}}'
    },
    # Detener
    {
        "role": "user",
        "content": "detente"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.0, "z": 0.0}}'
    },
    {
        "role": "user",
        "content": "para"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": 0.0, "y": 0.0, "z": 0.0}}'
    },
    # Movimientos compuestos
    {
        "role": "user",
        "content": "retrocede girando a la izquierda"
    },
    {
        "role": "assistant",
        "content": '{"name": "move_robot", "arguments": {"x": -0.2, "y": 0.0, "z": 0.3}}'
    },
    # Modos (CRÍTICO: mcf = apagar/seguro)
    {
        "role": "user",
        "content": "apaga los motores"
    },
    {
        "role": "assistant",
        "content": '{"name": "change_mode", "arguments": {"mode_name": "mcf"}}'
    },
    {
        "role": "user",
        "content": "modo seguro"
    },
    {
        "role": "assistant",
        "content": '{"name": "change_mode", "arguments": {"mode_name": "mcf"}}'
    },
    {
        "role": "user",
        "content": "activa el modo caminar"
    },
    {
        "role": "assistant",
        "content": '{"name": "change_mode", "arguments": {"mode_name": "normal"}}'
    }
]


def post_process_tool_call(tool_call: dict, original_command: str) -> dict:
    """
    Corrige errores comunes del LLM basados en patrones detectados

    Args:
        tool_call: Tool call generado por el LLM
        original_command: Comando original en texto

    Returns:
        Tool call corregido
    """
    import re

    name = tool_call.get("name")
    args = tool_call.get("arguments", {})

    if name == "move_robot":
        x = args.get("x", 0.0)
        y = args.get("y", 0.0)
        z = args.get("z", 0.0)

        cmd_lower = original_command.lower()

        # Detectar tipo de comando
        is_lateral_move = ("muévete" in cmd_lower or "camina" in cmd_lower or
                          "ve" in cmd_lower or "desplázate" in cmd_lower)
        has_left_right = ("izquierda" in cmd_lower or "derecha" in cmd_lower)
        is_turn = ("gira" in cmd_lower or "voltea" in cmd_lower or "rota" in cmd_lower)
        is_compound = ("girando" in cmd_lower or "retrocede" in cmd_lower or
                      "avanza" in cmd_lower or "adelante" in cmd_lower or
                      "atrás" in cmd_lower)

        # IMPORTANTE: No corregir comandos compuestos que ya tienen múltiples ejes
        # Si x!=0 Y z!=0, probablemente es un comando compuesto correcto
        has_multiple_axes = (abs(x) > 0 and abs(z) > 0) or (abs(y) > 0 and abs(z) > 0)

        if is_compound and has_multiple_axes:
            # Comando compuesto detectado con múltiples ejes, no tocar
            return tool_call

        # CORRECCIÓN 1: Movimiento lateral PURO confundido con adelante o giro
        # Solo si NO es un comando compuesto
        if is_lateral_move and has_left_right and not is_turn and not is_compound:
            # Debe ser movimiento lateral (eje Y), no frontal (X) ni giro (Z)
            if "izquierda" in cmd_lower:
                # Forzar movimiento lateral izquierdo
                if y <= 0 or x != 0 or z != 0:
                    args["x"] = 0.0
                    args["y"] = 0.3  # Lateral izquierda = y positivo
                    args["z"] = 0.0
            elif "derecha" in cmd_lower:
                # Forzar movimiento lateral derecho
                if y >= 0 or x != 0 or z != 0:
                    args["x"] = 0.0
                    args["y"] = -0.3  # Lateral derecha = y negativo
                    args["z"] = 0.0

        # CORRECCIÓN 2: Giro PURO con polaridad invertida
        # Solo si NO es un comando compuesto y solo tiene eje Z
        elif is_turn and has_left_right and not is_compound:
            # Solo debe tener Z, no X ni Y
            if "izquierda" in cmd_lower:
                # Giro izquierda debe ser Z positivo
                if z < 0:
                    args["z"] = abs(z)  # Invertir polaridad
                # Solo limpiar otros ejes si el comando es giro PURO
                if x != 0 or y != 0:
                    args["x"] = 0.0
                    args["y"] = 0.0
                # Si z es 0, asignar valor por defecto
                if args["z"] == 0:
                    args["z"] = 0.5
            elif "derecha" in cmd_lower:
                # Giro derecha debe ser Z negativo
                if z > 0:
                    args["z"] = -abs(z)  # Invertir polaridad
                # Solo limpiar otros ejes si el comando es giro PURO
                if x != 0 or y != 0:
                    args["x"] = 0.0
                    args["y"] = 0.0
                # Si z es 0, asignar valor por defecto
                if args["z"] == 0:
                    args["z"] = -0.5

    return tool_call


def validate_tool_call(tool_call: dict) -> tuple[bool, str]:
    """
    Valida que un tool call cumpla con los guardrails

    Args:
        tool_call: Diccionario con name y arguments

    Returns:
        (is_valid, error_message)
    """
    name = tool_call.get("name")
    args = tool_call.get("arguments", {})

    if not name:
        return False, "Missing tool name"

    if name == "move_robot":
        x = args.get("x", 0.0)
        y = args.get("y", 0.0)
        z = args.get("z", 0.0)

        if not (GUARDRAILS["safe_speed"].match(str(x)) and
                GUARDRAILS["safe_speed"].match(str(y)) and
                GUARDRAILS["safe_rotation"].match(str(z))):
            return False, f"Parameters exceeded safe limits: x={x}, y={y}, z={z}"

    elif name == "perform_action":
        action = args.get("action_name", "")
        if not GUARDRAILS["allowed_actions"].match(action):
            return False, f"Action '{action}' not in allowed list"

    elif name == "change_mode":
        mode = args.get("mode_name", "")
        if not GUARDRAILS["allowed_modes"].match(mode):
            return False, f"Mode '{mode}' not in allowed list"

    else:
        return False, f"Unknown tool: {name}"

    return True, "OK"
