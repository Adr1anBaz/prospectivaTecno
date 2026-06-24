import time
import logging
from prospectiva.bus.event_bus import EventBus

logger = logging.getLogger(__name__)


class MovementProcess:
    """
    Proceso que ejecuta movimientos secuenciales del robot.
    
    Placeholder: por ahora solo imprime los archivos que recibiría.
    Se integrará con el código existente de movimiento del robot.
    
    Flujo:
    1. Recibe evento MOVEMENT_SEQUENCE_READY con lista de archivos CSV
    2. Ejecuta cada archivo secuencialmente (uno tras otro)
    3. Publica MOVEMENT_COMPLETED cuando termina
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self._running = True
        self._current_sequence = []

    def run(self):
        logger.info("[MovementProcess] Started")
        while self._running:
            try:
                event = self.event_bus.get(timeout=1.0)
                if event is None:
                    continue
                event_type, payload = event
                if event_type == "MOVEMENT_SEQUENCE_READY":
                    self._execute_movement_sequence(payload)
            except Exception as e:
                logger.error(f"[MovementProcess] Error: {e}")
        logger.info("[MovementProcess] Stopped")

    def _execute_movement_sequence(self, payload: dict):
        """Ejecutar secuencia de movimientos."""
        files = payload.get("movement_files", [])
        end_node = payload.get("end_node", "unknown")
        
        if not files:
            logger.warning("[MovementProcess] No movement files to execute")
            return
        
        logger.info(f"[MovementProcess] Executing {len(files)} movement files to {end_node}")
        
        # Placeholder: en vez de ejecutar movimiento real, simula con prints
        for i, csv_file in enumerate(files, 1):
            logger.info(f"[MovementProcess] [{i}/{len(files)}] Executing: {csv_file}")
            # TODO: Aquí se integra el código real de movimiento
            # El código existente lee el CSV (tiempo, vel_x, yaw_z) y mueve el robot
            # For now, sleep to simulate execution
            time.sleep(0.5)
        
        logger.info(f"[MovementProcess] ✅ Sequence completed. Arrived at: {end_node}")
        
        # Notify completion
        self.event_bus.publish("MOVEMENT_COMPLETED", {
            "end_node": end_node,
            "movement_files": files,
        })

    def stop(self):
        self._running = False
