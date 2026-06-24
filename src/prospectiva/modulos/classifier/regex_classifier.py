import re
import time
import logging
from typing import Tuple, Dict, Any
from prospectiva.interfaces.classifier import IntentClassifier, Intent

logger = logging.getLogger(__name__)

class RegexIntentClassifier(IntentClassifier):
    """Deterministic regex-based intent classifier for 5 intents."""

    PATTERNS = {
        Intent.NAVEGAR_GIORNALE: re.compile(
            r"(ir|voy|dirigir|navegar|llévame|muestra|llevame|llevar).*"
            r"(giornale|periodico|noticias|diario|periódico)",
            re.IGNORECASE
        ),
        Intent.NAVEGAR_BIOMEDICA: re.compile(
            r"(ir|voy|dirigir|navegar|llévame|muestra|llevame|llevar).*"
            r"(biomedica|biomédica|medicina|lab|laboratorio|biomed)",
            re.IGNORECASE
        ),
        Intent.COMANDO_SIT: re.compile(
            r"(siéntate|sentar|sienta|sientate|sientese|sientése)",
            re.IGNORECASE
        ),
        Intent.COMANDO_DANCE: re.compile(
            r"(baila|bailar|danza|dance|muevete|muévete)",
            re.IGNORECASE
        ),
    }

    def classify(self, text: str) -> Tuple[Intent, Dict[str, Any]]:
        start = time.time()
        for intent, pattern in self.PATTERNS.items():
            if pattern.search(text):
                elapsed = (time.time() - start) * 1000
                logger.info(f"[Classifier] Intent={intent.value} in {elapsed:.1f}ms")
                return intent, {"confidence": 1.0, "match": text}
        elapsed = (time.time() - start) * 1000
        logger.info(f"[Classifier] Intent=HABLAR (default) in {elapsed:.1f}ms")
        return Intent.HABLAR, {"confidence": 1.0, "match": None}
