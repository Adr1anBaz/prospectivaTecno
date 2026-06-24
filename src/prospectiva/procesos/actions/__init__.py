import logging
from typing import Dict, Any

from prospectiva.procesos.actions.action_executor import ActionExecutor
from prospectiva.procesos.actions.robot_actions import RobotActions
from prospectiva.procesos.actions.navigation_actions import NavigationActions
from prospectiva.utils.route_client import RouteClient

logger = logging.getLogger(__name__)

def create_default_executor(route_client: RouteClient | None = None) -> ActionExecutor:
    """
    Crear un ActionExecutor con las acciones por defecto registradas.
    
    Args:
        route_client: Cliente de Route API para navegación real
    
    Uso:
        executor = create_default_executor(route_client)
        result = executor.execute("COMANDO_SIT", {"text": "siéntate"})
    """
    executor = ActionExecutor()
    
    # Crear instancia de NavigationActions con RouteClient
    nav_actions = NavigationActions(route_client)
    
    # Registrar acciones de navegación
    executor.register("NAVEGAR_BIOMEDICA", lambda p: nav_actions.navigate({**p, "destination": "BIOMEDICA"}))
    executor.register("NAVEGAR_GIORNALE", lambda p: nav_actions.navigate({**p, "destination": "GIORNALE"}))
    executor.register("NAVEGAR_BIBLIOTECA", lambda p: nav_actions.navigate({**p, "destination": "BIBLIOTECA"}))
    executor.register("NAVEGAR_CAFETERIA", lambda p: nav_actions.navigate({**p, "destination": "CAFETERIA"}))
    
    # Registrar acciones del robot
    executor.register("COMANDO_SIT", RobotActions.sit)
    executor.register("COMANDO_DANCE", RobotActions.dance)
    executor.register("COMANDO_STAND", RobotActions.stand)
    executor.register("COMANDO_WAVE", RobotActions.wave)
    executor.register("COMANDO_WALK", RobotActions.walk)
    executor.register("COMANDO_STOP", RobotActions.stop)
    
    logger.info(f"[ActionFactory] Created executor with {len(executor.list_registered())} actions")
    return executor
