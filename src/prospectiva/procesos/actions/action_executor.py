import logging
import traceback
from typing import Dict, Callable, Any

logger = logging.getLogger(__name__)

class ActionExecutor:
    """
    Ejecutor de acciones registradas por intent.
    
    Permite registrar handlers para cada intent y ejecutarlos
    cuando el classifier detecta un comando.
    
    Ejemplo de uso:
        executor = ActionExecutor()
        executor.register("NAVEGAR_BIOMEDICA", navigate_to_biomedica)
        executor.register("COMANDO_SIT", robot_sit)
        executor.execute("NAVEGAR_BIOMEDICA", {"text": "llévame a biomédica"})
    """

    def __init__(self):
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._history: list[Dict[str, Any]] = []

    def register(self, intent: str, handler: Callable[[Dict[str, Any]], Any]):
        """Registrar un handler para un intent."""
        self._handlers[intent] = handler
        logger.info(f"[ActionExecutor] Registered handler for {intent}")

    def execute(self, intent: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar el handler para un intent."""
        handler = self._handlers.get(intent)
        if not handler:
            logger.warning(f"[ActionExecutor] No handler for intent: {intent}")
            return {"success": False, "error": f"No handler for {intent}"}
        
        try:
            logger.info(f"[ActionExecutor] Executing {intent} with params: {params}")
            result = handler(params)
            action_record = {
                "intent": intent,
                "params": params,
                "result": result,
                "timestamp": __import__('time').time(),
            }
            self._history.append(action_record)
            logger.info(f"[ActionExecutor] {intent} executed successfully: {result}")
            return {"success": True, "result": result, "intent": intent}
        except Exception as e:
            logger.error(f"[ActionExecutor] Error executing {intent}: {e}")
            logger.error(traceback.format_exc())
            return {"success": False, "error": str(e), "intent": intent}

    def get_history(self) -> list[Dict[str, Any]]:
        """Obtener historial de acciones ejecutadas."""
        return self._history.copy()

    def list_registered(self) -> list[str]:
        """Listar intents registrados."""
        return list(self._handlers.keys())
