import os
import time
import logging
from typing import Any, Dict, List

import httpx

logger = logging.getLogger(__name__)


class RouteClient:
    """
    Cliente para la API independiente de cálculo de ruta.
    
    Recibe nombres de nodos (strings) y devuelve la lista de archivos CSV
    de movimiento para ir del nodo inicio al nodo destino.
    """

    def __init__(self, base_url: str | None = None, timeout: float = 10.0):
        self.base_url = base_url or os.getenv("ROUTE_API_URL", "http://localhost:8081")
        self.timeout = timeout
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)
        self._available = False
        try:
            self._check_health()
        except Exception as e:
            logger.warning(f"[RouteClient] Route API not available at {self.base_url}: {e}")

    def _check_health(self) -> bool:
        """Check if Route API is up."""
        try:
            resp = self._client.get("/api/health")
            if resp.status_code == 200:
                self._available = True
                logger.info(f"[RouteClient] Route API connected at {self.base_url}")
                return True
        except Exception:
            pass
        self._available = False
        return False

    def is_available(self) -> bool:
        return self._available

    def calculate_route(self, start_node: str, end_node: str) -> Dict[str, Any]:
        """
        Calcular ruta entre dos nodos.
        
        Args:
            start_node: Nombre del nodo de inicio (ej. "pasillo_a")
            end_node: Nombre del nodo de destino (ej. "giornale")
        
        Returns:
            {
                "movement_files": ["ruta_001.csv", "ruta_002.csv", ...],
                "path": ["pasillo_a", "pasillo_b", "giornale"],
                "estimated_time": 45.0,
                "success": True/False,
                "error": "mensaje" (si falla)
            }
        """
        if not self._available:
            return {
                "success": False,
                "error": "Route API not available",
                "movement_files": [],
                "path": [],
                "estimated_time": 0,
            }
        
        try:
            logger.info(f"[RouteClient] Calculating route: {start_node} → {end_node}")
            resp = self._client.post(
                "/api/routes/calculate",
                json={"start": start_node, "end": end_node}
            )
            if resp.status_code == 200:
                data = resp.json()
                data["success"] = True
                logger.info(f"[RouteClient] Route calculated: {len(data.get('movement_files', []))} files")
                return data
            else:
                logger.error(f"[RouteClient] Route API error: {resp.status_code} - {resp.text}")
                return {
                    "success": False,
                    "error": f"Route API returned {resp.status_code}",
                    "movement_files": [],
                    "path": [],
                    "estimated_time": 0,
                }
        except Exception as e:
            logger.error(f"[RouteClient] Route calculation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "movement_files": [],
                "path": [],
                "estimated_time": 0,
            }

    def __del__(self):
        self._client.close()
