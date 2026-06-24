import json
import time
from typing import List, Dict, Any


class ConversationMemory:
    """
    Memoria de conversación completa de la sesión.
    
    Guarda:
    - Historial de turnos (user/assistant)
    - Posición actual del robot (nombre del nodo del grafo)
    - Limpieza automática al reiniciar
    """

    def __init__(self, max_turns: int = 20):
        self._history: List[Dict[str, Any]] = []
        self._current_node: str = "base"
        self._max_turns = max_turns

    def add_turn(self, role: str, text: str, metadata: dict | None = None):
        """Agregar un turno al historial."""
        turn = {
            "role": role,
            "text": text,
            "timestamp": time.time(),
        }
        if metadata:
            turn["metadata"] = metadata
        self._history.append(turn)
        # Mantener solo los últimos N turnos
        if len(self._history) > self._max_turns:
            self._history = self._history[-self._max_turns:]

    def get_history(self, n: int | None = None) -> List[Dict[str, Any]]:
        """Obtener historial (últimos n turnos)."""
        if n is None:
            return self._history.copy()
        return self._history[-n:]

    def get_formatted_history(self, n: int | None = None) -> str:
        """Obtener historial como texto formateado para el prompt."""
        turns = self.get_history(n)
        lines = []
        for turn in turns:
            lines.append(f"{turn['role'].upper()}: {turn['text']}")
        return "\n".join(lines)

    def get_last_turn(self) -> Dict[str, Any] | None:
        """Obtener el último turno."""
        if not self._history:
            return None
        return self._history[-1]

    def get_last_user_query(self) -> str:
        """Obtener la última consulta del usuario."""
        for turn in reversed(self._history):
            if turn["role"] == "user":
                return turn["text"]
        return ""

    def get_current_node(self) -> str:
        """Obtener el nodo actual del robot."""
        return self._current_node

    def set_current_node(self, node: str):
        """Actualizar el nodo actual del robot (después de navegar)."""
        self._current_node = node

    def clear(self):
        """Limpiar todo el historial."""
        self._history = []

    def get_state(self) -> Dict[str, Any]:
        """Obtener el estado completo para debugging."""
        return {
            "current_node": self._current_node,
            "total_turns": len(self._history),
            "history": self._history,
        }

    def __repr__(self):
        return f"ConversationMemory(turns={len(self._history)}, node={self._current_node})"
