import time
import json
from typing import Dict, Any, List
from datetime import datetime

class ToolUsageTracker:
    """
    Registra qué herramientas llamó el modelo LLM.
    
    Cada entrada incluye:
    - timestamp
    - nombre de la herramienta
    - argumentos
    - resultado
    - duración
    """

    def __init__(self):
        self._calls: List[Dict[str, Any]] = []

    def record(self, tool_name: str, arguments: Dict[str, Any], 
               result: Any, duration_ms: float = 0):
        """Registrar una llamada a herramienta."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "arguments": arguments,
            "result": self._truncate_result(result),
            "duration_ms": duration_ms,
        }
        self._calls.append(entry)

    def get_calls(self) -> List[Dict[str, Any]]:
        """Obtener todas las llamadas registradas."""
        return self._calls.copy()

    def get_summary(self) -> str:
        """Obtener resumen formateado de las llamadas."""
        if not self._calls:
            return "🛠️ No se llamaron herramientas"
        
        lines = [
            "",
            "=" * 60,
            "  🛠️ HERRAMIENTAS LLAMADAS POR EL MODELO",
            "=" * 60,
        ]
        
        for i, call in enumerate(self._calls, 1):
            lines.append(f"  {i}. {call['tool_name']}")
            lines.append(f"     Args: {json.dumps(call['arguments'], ensure_ascii=False)}")
            lines.append(f"     Result: {call['result']}")
            lines.append(f"     Time: {call['duration_ms']:.0f}ms")
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)

    def get_tool_names(self) -> List[str]:
        """Obtener lista de nombres de herramientas usadas."""
        return [call["tool_name"] for call in self._calls]

    def clear(self):
        """Limpiar el registro."""
        self._calls = []

    def count(self) -> int:
        """Número de llamadas registradas."""
        return len(self._calls)

    def _truncate_result(self, result: Any, max_len: int = 100) -> str:
        """Truncar resultado para logging."""
        text = json.dumps(result, ensure_ascii=False) if not isinstance(result, str) else result
        if len(text) > max_len:
            return text[:max_len] + "..."
        return text

    def __repr__(self):
        return f"ToolUsageTracker(calls={len(self._calls)})"
