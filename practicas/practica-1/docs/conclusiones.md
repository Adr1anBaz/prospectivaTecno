---
layout: default
title: 6. Conclusiones
nav_order: 7
---

# Conclusiones de la Práctica

## Conclusión General

La realización de esta práctica permite consolidar una visión crítica y técnica sobre el panorama actual de la Inteligencia Artificial Generativa y los Modelos de Lenguaje de Gran Escala (LLMs). La experimentación directa con herramientas de despliegue local como **Ollama** demuestra que la democratización del acceso a la IA no es solo una tendencia teórica, sino una realidad técnica viable en hardware convencional.

A partir de los puntos analizados, se desprenden tres grandes pilares de aprendizaje:

* **El balance entre recursos y cognición (*Trade-off*):** El rendimiento de modelos como Qwen 2.5 7B y Llama 3.2 3B en español evidencia que el éxito de un modelo no depende exclusivamente de un tamaño masivo, sino de la calidad de su arquitectura y del balance multilingüe en sus datos de entrenamiento. El tamaño del modelo dicta una relación inversa estricta entre la velocidad de inferencia y la profundidad semántica, obligando al ingeniero a seleccionar la arquitectura basándose en las restricciones de hardware y la complejidad de la tarea.
* **Viabilidad de la soberanía de datos:** La ejecución local mitiga de forma definitiva las limitantes más críticas de las APIs comerciales en entornos profesionales: la privacidad absoluta de la información y la dependencia financiera/operativa de terceros. Si bien las APIs en la nube (como GPT-4 o Claude) se mantienen insustituibles para tareas que requieren razonamiento lógico abstracto de frontera o capacidades multimodales masivas, el ecosistema *open-source* local es una alternativa madura y robusta para el prototipado rápido y el desarrollo confidencial.
* **Responsabilidad técnica y académica:** La comprensión de conceptos estructurales —desde los *embeddings* hasta el mecanismo de auto-atención en los *Transformers*— disipa la percepción del LLM como una entidad de conocimiento estático. Al ser herramientas probabilísticas, su integración en flujos académicos o de ingeniería exige una postura de supervisión constante. Los modelos deben ser tratados como catalizadores de productividad y asistentes de optimización, pero jamás como fuentes únicas de validación factual o científica.

En última instancia, el panorama de la IA generativa local abre un horizonte altamente prometedor para la ingeniería contemporánea. La optimización actual de los modelos pequeños (1B - 3B) no solo redefine el desarrollo de software convencional, sino que sienta las bases para trasladar la inferencia inteligente al borde (*edge computing*), permitiendo vislumbrar un futuro cercano donde la autonomía cognitiva pueda ser integrada directamente en sistemas embebidos, robótica y hardware dedicado de manera eficiente y privada.