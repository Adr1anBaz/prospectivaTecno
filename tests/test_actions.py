import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from prospectiva.procesos.actions.action_executor import ActionExecutor
from prospectiva.procesos.actions.robot_actions import RobotActions
from prospectiva.procesos.actions.navigation_actions import NavigationActions
from prospectiva.modulos.classifier.configurable_classifier import ConfigurableClassifier


def test_actions():
    """Test the action system."""
    print("=" * 60)
    print("TEST ACTION SYSTEM")
    print("=" * 60)
    
    # Create executor with default actions
    from prospectiva.procesos.actions import create_default_executor
    executor = create_default_executor()
    
    print(f"\nRegistered actions: {executor.list_registered()}")
    
    # Test classifications
    classifier = ConfigurableClassifier(config_path="config/commands.yaml")
    
    test_phrases = [
        "siéntate",
        "baila",
        "llévame a biomédica",
        "hola qué tal",
    ]
    
    for phrase in test_phrases:
        intent, meta = classifier.classify(phrase)
        print(f"\n🎯 Phrase: '{phrase}'")
        print(f"   Intent: {intent.value}")
        
        if intent.value.startswith("COMANDO") or intent.value.startswith("NAVEGAR"):
            result = executor.execute(intent.value, {"text": phrase})
            print(f"   Action result: {result}")
        else:
            print(f"   → LLM will handle this")
    
    print("\n" + "=" * 60)
    print("TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_actions()
