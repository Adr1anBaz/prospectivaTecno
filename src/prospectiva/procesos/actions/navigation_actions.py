import logging
import time
from typing import Dict, Any

from prospectiva.utils.route_client import RouteClient

logger = logging.getLogger(__name__)

class NavigationActions:
    """
    Acciones de navegación autónoma.
    
    Integra con la Route API para calcular rutas reales entre nodos
    y devolver la lista de archivos CSV de movimiento.
    """

    # Mapa de destinos: ID del classifier → nombre del nodo en el grafo
    DESTINATIONS = {
        "BIOMEDICA": "biomedica",
        "GIORNALE": "giornale",
        "BIBLIOTECA": "biblioteca",
        "CAFETERIA": "cafeteria",
    }

    # Nombres legibles para TTS
    DESTINATIONS_NAMES = {
        "biomedica": "Edificio de Biomédica",
        "giornale": "Edificio Giornale",
        "biblioteca": "Biblioteca Central",
        "cafeteria": "Cafetería",
    }

    def __init__(self, route_client: RouteClient | None = None):
        self.route_client = route_client

    def navigate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Navegar a un destino usando la Route API.
        
        params:
            - destination: str (BIOMEDICA, GIORNALE, etc.)
            - text: str (texto original del usuario)
            - current_node: str (nodo actual del robot)
        """
        destination_id = params.get("destination", "UNKNOWN")
        current_node = params.get("current_node", "base")
        node_name = NavigationActions.DESTINATIONS.get(destination_id)
        
        if not node_name:
            logger.warning(f"[NavigationActions] Unknown destination: {destination_id}")
            return {
                "action": "navigate",
                "status": "failed",
                "error": f"Unknown destination: {destination_id}",
                "destination": destination_id,
            }
        
        dest_name = NavigationActions.DESTINATIONS_NAMES.get(node_name, node_name)
        logger.info(f"[NavigationActions] 🗺️ NAVIGATE: {dest_name}")
        
        # Calcular ruta usando RouteClient
        if self.route_client and self.route_client.is_available():
            route_result = self.route_client.calculate_route(current_node, node_name)
            
            if route_result.get("success"):
                logger.info(f"[NavigationActions] Route calculated: {len(route_result.get('movement_files', []))} files")
                return {
                    "action": "navigate",
                    "status": "completed",
                    "destination": destination_id,
                    "node": node_name,
                    "name": dest_name,
                    "movement_files": route_result.get("movement_files", []),
                    "path": route_result.get("path", []),
                    "estimated_time": route_result.get("estimated_time", 0),
                }
            else:
                logger.warning(f"[NavigationActions] Route calculation failed: {route_result.get('error')}")
                return {
                    "action": "navigate",
                    "status": "failed",
                    "error": route_result.get("error", "Route calculation failed"),
                    "destination": destination_id,
                }
        else:
            # Fallback: Route API not available
            logger.info("[NavigationActions] Route API unavailable, returning mock route")
            time.sleep(1.0)
            return {
                "action": "navigate",
                "status": "completed",
                "destination": destination_id,
                "node": node_name,
                "name": dest_name,
                "movement_files": ["ruta_mock.csv"],
                "path": [current_node, node_name],
                "estimated_time": 45.0,
            }

    def get_location(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener ubicación actual."""
        current_node = params.get("current_node", "unknown")
        logger.info(f"[NavigationActions] 📍 GET_LOCATION: {current_node}")
        return {
            "action": "get_location",
            "status": "completed",
            "node": current_node,
        }

    def list_destinations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Listar destinos disponibles."""
        logger.info("[NavigationActions] 📋 LIST_DESTINATIONS")
        return {
            "action": "list_destinations",
            "status": "completed",
            "destinations": list(NavigationActions.DESTINATIONS.keys()),
            "nodes": list(NavigationActions.DESTINATIONS.values()),
        }

    def navigate_to_node(self, current_node: str, end_node: str) -> Dict[str, Any]:
        """
        Navegar directamente a un nodo por nombre (usado por LLM inference).
        
        Args:
            current_node: Nodo actual (ej. "pasillo_a")
            end_node: Nodo destino (ej. "giornale")
        
        Returns:
            Dict con resultado de la ruta
        """
        dest_name = NavigationActions.DESTINATIONS_NAMES.get(end_node, end_node)
        logger.info(f"[NavigationActions] 🗺️ NAVIGATE_TO_NODE: {current_node} → {end_node}")
        
        if self.route_client and self.route_client.is_available():
            route_result = self.route_client.calculate_route(current_node, end_node)
            
            if route_result.get("success"):
                return {
                    "action": "navigate",
                    "status": "completed",
                    "node": end_node,
                    "name": dest_name,
                    "movement_files": route_result.get("movement_files", []),
                    "path": route_result.get("path", []),
                    "estimated_time": route_result.get("estimated_time", 0),
                }
            else:
                return {
                    "action": "navigate",
                    "status": "failed",
                    "error": route_result.get("error", "Route calculation failed"),
                    "node": end_node,
                }
        else:
            logger.info("[NavigationActions] Route API unavailable, returning mock route")
            return {
                "action": "navigate",
                "status": "completed",
                "node": end_node,
                "name": dest_name,
                "movement_files": ["ruta_mock.csv"],
                "path": [current_node, end_node],
                "estimated_time": 45.0,
            }
