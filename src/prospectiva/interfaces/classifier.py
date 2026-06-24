from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, Dict, Any

class Intent(Enum):
    HABLAR = "HABLAR"
    # Navegación
    NAVEGAR_GIORNALE = "NAVEGAR_GIORNALE"
    NAVEGAR_BIOMEDICA = "NAVEGAR_BIOMEDICA"
    NAVEGAR_BIBLIOTECA = "NAVEGAR_BIBLIOTECA"
    NAVEGAR_CAFETERIA = "NAVEGAR_CAFETERIA"
    # Comandos del robot
    COMANDO_SIT = "COMANDO_SIT"
    COMANDO_DANCE = "COMANDO_DANCE"
    COMANDO_STAND = "COMANDO_STAND"
    COMANDO_WAVE = "COMANDO_WAVE"
    COMANDO_WALK = "COMANDO_WALK"
    COMANDO_STOP = "COMANDO_STOP"

class IntentClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> Tuple[Intent, Dict[str, Any]]:
        """Classify text into an intent. Returns (intent, metadata)."""
        ...
