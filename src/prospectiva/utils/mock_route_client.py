import json
import time
from typing import Any, Dict, List
from prospectiva.utils.route_client import RouteClient

class MockRouteClient(RouteClient):
    """
    Mock Route Client para pruebas sin el servidor real.
    Devuelve rutas ficticias entre nodos.
    """

    def __init__(self, base_url: str | None = None, timeout: float = 10.0):
        # Don't call super().__init__ to avoid HTTP check
        self.base_url = "mock://localhost"
        self._available = True
        self._mock_routes = self._load_mock_routes()

    def _load_mock_routes(self) -> Dict:
        """Cargar rutas mock predefinidas."""
        return {
            ("base", "giornale"): {
                "movement_files": ["ruta_base_pasillo_a.csv", "ruta_pasillo_a_giornale.csv"],
                "path": ["base", "pasillo_a", "giornale"],
                "estimated_time": 30.0,
            },
            ("base", "biomedica"): {
                "movement_files": ["ruta_base_pasillo_c.csv", "ruta_pasillo_c_biomedica.csv"],
                "path": ["base", "pasillo_c", "biomedica"],
                "estimated_time": 45.0,
            },
            ("base", "biblioteca"): {
                "movement_files": ["ruta_base_pasillo_b.csv", "ruta_pasillo_b_biblioteca.csv"],
                "path": ["base", "pasillo_b", "biblioteca"],
                "estimated_time": 25.0,
            },
            ("base", "cafeteria"): {
                "movement_files": ["ruta_base_pasillo_b.csv", "ruta_pasillo_b_cafeteria.csv"],
                "path": ["base", "pasillo_b", "cafeteria"],
                "estimated_time": 20.0,
            },
            ("pasillo_a", "giornale"): {
                "movement_files": ["ruta_pasillo_a_giornale.csv"],
                "path": ["pasillo_a", "giornale"],
                "estimated_time": 15.0,
            },
            ("pasillo_a", "biblioteca"): {
                "movement_files": ["ruta_pasillo_a_base.csv", "ruta_base_pasillo_b.csv", "ruta_pasillo_b_biblioteca.csv"],
                "path": ["pasillo_a", "base", "pasillo_b", "biblioteca"],
                "estimated_time": 40.0,
            },
            ("giornale", "biblioteca"): {
                "movement_files": ["ruta_giornale_pasillo_a.csv", "ruta_pasillo_a_base.csv", "ruta_base_pasillo_b.csv", "ruta_pasillo_b_biblioteca.csv"],
                "path": ["giornale", "pasillo_a", "base", "pasillo_b", "biblioteca"],
                "estimated_time": 50.0,
            },
            ("giornale", "cafeteria"): {
                "movement_files": ["ruta_giornale_pasillo_a.csv", "ruta_pasillo_a_base.csv", "ruta_base_pasillo_b.csv", "ruta_pasillo_b_cafeteria.csv"],
                "path": ["giornale", "pasillo_a", "base", "pasillo_b", "cafeteria"],
                "estimated_time": 55.0,
            },
            ("biomedica", "giornale"): {
                "movement_files": ["ruta_biomedica_pasillo_c.csv", "ruta_pasillo_c_base.csv", "ruta_base_pasillo_a.csv", "ruta_pasillo_a_giornale.csv"],
                "path": ["biomedica", "pasillo_c", "base", "pasillo_a", "giornale"],
                "estimated_time": 60.0,
            },
            ("biblioteca", "cafeteria"): {
                "movement_files": ["ruta_biblioteca_pasillo_b.csv", "ruta_pasillo_b_cafeteria.csv"],
                "path": ["biblioteca", "pasillo_b", "cafeteria"],
                "estimated_time": 15.0,
            },
        }

    def is_available(self) -> bool:
        return True

    def calculate_route(self, start_node: str, end_node: str) -> Dict[str, Any]:
        """Mock route calculation."""
        key = (start_node, end_node)
        
        if key in self._mock_routes:
            route = self._mock_routes[key]
            return {
                "success": True,
                "movement_files": route["movement_files"],
                "path": route["path"],
                "estimated_time": route["estimated_time"],
            }
        else:
            # Generic fallback: generate a simple route
            return {
                "success": True,
                "movement_files": [f"ruta_{start_node}_{end_node}.csv"],
                "path": [start_node, end_node],
                "estimated_time": 30.0,
            }

    def __del__(self):
        """Override parent __del__ to avoid httpx cleanup error."""
        pass
