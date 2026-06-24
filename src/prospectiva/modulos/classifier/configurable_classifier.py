import os
import yaml
import logging
import re
from typing import Dict, Tuple, List
from prospectiva.interfaces.classifier import IntentClassifier, Intent

logger = logging.getLogger(__name__)

class ConfigurableClassifier(IntentClassifier):
    """
    Classifier que carga intents desde un archivo YAML.
    
    Permite agregar nuevos comandos editando config/commands.yaml
    sin tocar código.
    """

    def __init__(self, config_path: str = "config/commands.yaml"):
        self.config_path = config_path
        self._patterns: Dict[str, List[str]] = {}
        self._commands: List[Dict] = []
        self._load_config()

    def _load_config(self):
        """Cargar configuración desde YAML."""
        if not os.path.exists(self.config_path):
            logger.warning(f"[ConfigurableClassifier] Config not found: {self.config_path}")
            return
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            
            commands = config.get("commands", [])
            for cmd in commands:
                name = cmd.get("name", "HABLAR")
                patterns = cmd.get("patterns", [])
                self._patterns[name] = patterns
                self._commands.append(cmd)
            
            logger.info(f"[ConfigurableClassifier] Loaded {len(self._commands)} commands from {self.config_path}")
        except Exception as e:
            logger.error(f"[ConfigurableClassifier] Error loading config: {e}")
            # Fallback a defaults
            self._load_defaults()

    def _load_defaults(self):
        """Cargar patrones por defecto."""
        self._patterns = {
            "NAVEGAR_BIOMEDICA": ["biomédica", "biomedica", "edificio de biomédica"],
            "NAVEGAR_GIORNALE": ["giornale", "edificio giornale"],
            "NAVEGAR_BIBLIOTECA": ["biblioteca", "biblio"],
            "NAVEGAR_CAFETERIA": ["cafetería", "cafeteria", "comer"],
            "COMANDO_SIT": ["siéntate", "sentarse", "sientate"],
            "COMANDO_DANCE": ["baila", "bailar", "danza"],
            "COMANDO_STAND": ["pararte", "levántate", "ponte de pie"],
            "COMANDO_WAVE": ["saluda", "saludar"],
            "COMANDO_WALK": ["camina", "caminar", "anda"],
            "COMANDO_STOP": ["detente", "parar", "alto"],
        }
        logger.info("[ConfigurableClassifier] Loaded default patterns")

    def classify(self, text: str) -> Tuple[Intent, Dict]:
        """Clasificar texto usando patrones del YAML."""
        text_lower = text.lower().strip()
        text_clean = re.sub(r'[^\w\sáéíóúñü]', '', text_lower)
        
        for intent_name, patterns in self._patterns.items():
            for pattern in patterns:
                pattern_clean = re.sub(r'[^\w\sáéíóúñü]', '', pattern.lower())
                if pattern_clean in text_clean or pattern in text_lower:
                    logger.info(f"[ConfigurableClassifier] Match: '{pattern}' -> {intent_name}")
                    return Intent(intent_name), {"pattern": pattern, "text": text}
        
        return Intent("HABLAR"), {"text": text}

    def get_command_info(self, intent_name: str) -> Dict:
        """Obtener información de un comando por su nombre."""
        for cmd in self._commands:
            if cmd.get("name") == intent_name:
                return cmd
        return {}

    def list_commands(self) -> List[Dict]:
        """Listar todos los comandos configurados."""
        return self._commands.copy()
