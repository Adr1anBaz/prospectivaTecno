---
layout: default
title: 5. Reflexión
nav_order: 6
---

# Reflexión: Práctica 1 - Panorama de IA Generativa y LLM

Análisis personal sobre la experiencia de trabajar con modelos de lenguaje locales.

---

## 1. Facilidad de Instalación

**¿Qué tan fácil fue instalar y usar Ollama?**

**Respuesta:**
La instalación de Ollama fue un proceso sumamente sencillo e intuitivo, destacando por su enfoque *plug-and-play* tanto en la descarga del ejecutable como en su configuración inicial en el sistema. La documentación oficial es minimalista pero sumamente clara, permitiendo interactuar con el ecosistema a través de la terminal de manera inmediata.

La descarga de los modelos mediante el comando `ollama run` es eficiente, automatizando la gestión de manifiestos y capas de los modelos. El principal reto técnico radicó en el tiempo de descarga debido al peso de los archivos de parámetros más grandes (como Phi-4 de 14B), y en asegurar el espacio suficiente en el disco duro. Fuera de la espera por la tasa de transferencia de red, el entorno de Ollama demostró ser una abstracción excelente que elimina por completo la complejidad de configurar entornos virtuales de Python o dependencias de CUDA de forma manual.

---

## 2. Desempeño en Español

**¿Qué modelo(s) respondieron mejor en español? ¿Por qué crees que fue así?**

**Respuesta:**
Los modelos con mejor desempeño en español fueron **Qwen 2.5 7B** y **Llama 3.2 3B**. 

Qwen 2.5 7B destacó con una naturalidad lingüística sobresaliente, precisión en la jerga académica y una gramática impecable. Por su parte, Llama 3.2 3B ofreció respuestas estructuradas y coherentes que sorprenden gratamente considerando su escala compacta. Este rendimiento superior se debe a que ambos modelos fueron entrenados explícitamente con conjuntos de datos masivos y diversos que incluyen una fuerte representación multilingüe. 

En contraste, modelos como **TinyLlama (1.1B)** y **Mistral 7B** mostraron limitaciones; el primero por su falta de capacidad matemática y semántica para mantener el contexto en español (tendiendo a mezclar palabras en inglés o alucinar), y el segundo porque su alineación y datos de entrenamiento están fuertemente sesgados hacia el inglés y el francés.

---

## 3. Diferencias de Tamaño de Modelo

**¿Cómo afecta el tamaño del modelo (número de parámetros) a la velocidad y calidad de las respuestas?**

**Respuesta:**
El tamaño del modelo dicta un *trade-off* directo e inversamente proporcional entre la velocidad de inferencia (tokens por segundo) y la profundidad cognitiva de las respuestas:

* **Modelos Pequeños (1B - 3B):** Modelos como TinyLlama y Gemma 2 2B ofrecen una velocidad de respuesta casi instantánea con un consumo de RAM mínimo (~2-4 GB), permitiendo su ejecución fluida en hardware convencional. Sin embargo, su capacidad de razonamiento lógico es superficial y simplista.
* **Modelos Medianos y Grandes (7B - 14B):** Modelos como Qwen 2.5 7B y Phi-4 (14B) consumen una cantidad de recursos crítica (exigiendo entre 8 GB y 16 GB de RAM/VRAM). La velocidad de inferencia cae notablemente si se ejecutan puramente en CPU, pero la calidad, coherencia, estructuración y riqueza argumentativa de las respuestas es drásticamente superior.

La regla general observada es: a mayor cantidad de parámetros, el modelo cuenta con más "conexiones" para procesar sutilezas semánticas, pagando el precio en una mayor latencia de cómputo.

---

## 4. Importancia de las Licencias

**¿Por qué es importante revisar la licencia de un modelo antes de usarlo?**

**Respuesta:**
Revisar la licencia es un paso crítico en ingeniería de software y ciencia de datos, ya que delimita los derechos legales de explotación, modificación y privacidad de la tecnología. No todos los modelos de "código abierto" (*open-source*) o disponibles públicamente permiten los mismos usos.

Por ejemplo, modelos bajo licencias altamente permisivas como **Apache 2.0** (Qwen 2.5, Mistral, TinyLlama) o **MIT** (Phi-4) otorgan total libertad para su integración en productos comerciales, modificaciones del código base y redistribución sin regalías. Por el contrario, licencias comunitarias como la de **Llama 3.2** o los términos de uso de **Gemma 2**, si bien son permisivas para desarrollo e investigación, imponen restricciones explícitas (como topes de usuarios comerciales activos al mes o prohibiciones de usar sus salidas para entrenar modelos competidores), lo que podría acarrear contingencias legales millonarias en entornos corporativos si se ignoran.

---

## 5. LLMs como Fuente Académica

**¿Por qué los LLMs no deben ser la única fuente de información en trabajos académicos?**

**Respuesta:**
Los LLMs son herramientas probabilísticas de generación de texto (predicen la palabra más coherente a continuación), no bases de datos de conocimiento estático indexado. Por ende, presentan limitaciones fundamentales que invalidan su uso como fuente primaria única:

1.  **Alucinaciones:** Generan con absoluta elocuencia datos, fechas, ecuaciones e incluso citas bibliográficas completamente inexistentes.
2.  **Falta de Trazabilidad:** No proveen de forma nativa referencias verificables a artículos indexados (*peer-reviewed*), impidiendo la validación de fuentes primarias.
3.  **Fecha de Corte (Knowledge Cutoff):** Su conocimiento está limitado temporalmente al momento en que finalizó su entrenamiento, ignorando descubrimientos o eventos recientes.
4.  **Sesgos Inherentes:** Replican de manera opaca los sesgos e imprecisiones de los datos con los que fueron alimentados en internet.

Su rol académico debe ser el de asistentes de redacción, estructuración y lluvia de ideas, pero jamás el de autoridades de validación factual.

---

## 6. Ejecución Local vs. APIs en la Nube

**¿Qué ventajas y limitaciones tiene ejecutar modelos localmente (como con Ollama) comparado con usar APIs en la nube (como ChatGPT, Claude)?**

### Ventajas de Ejecución Local:
1.  **Privacidad y Seguridad de Datos Absoluta:** Los datos procesados jamás salen de la máquina local, eliminando el riesgo de filtraciones o telemetría corporativa.
2.  **Cero Costos de Operación por Inferencia:** No depende de suscripciones recurrentes ni de cobros por volumen de *tokens* consumidos.
3.  **Disponibilidad Offline:** Permite trabajar de manera continua y autónoma sin requerir una conexión activa a internet.

### Limitaciones de Ejecución Local:
1.  **Dependencia Estricta del Hardware:** El rendimiento está severamente limitado por las capacidades de la CPU, la memoria RAM y la VRAM de la GPU del equipo.
2.  **Menor Capacidad Cognitiva:** Los modelos que se pueden ejecutar localmente de forma fluida (usualmente hasta 14B) tienen un razonamiento inferior comparado con los macro-modelos de la nube.
3.  **Consumo Energético y Térmico:** La inferencia continua exige un alto consumo eléctrico y eleva drásticamente las temperaturas del hardware local.

### Ventajas de APIs en la Nube:
1.  **Acceso a Modelos de Frontera (SOTA):** Permite interactuar con arquitecturas masivas de cientos de miles de millones de parámetros (como GPT-4 o Claude 3.5 Sonnet) con capacidades lógicas superiores.
2.  **Velocidad de Inferencia Escalable:** El procesamiento ocurre en centros de datos optimizados, ofreciendo respuestas rápidas sin importar la complejidad conceptual.
3.  **Capacidades Multimodales Nativas:** Integración fluida e inmediata de visión por computadora, análisis de audio avanzado y ejecución de código en sandbox.

### Limitaciones de APIs en la Nube:
1.  **Dependencia de Conexión a Internet:** Cualquier interrupción en la red detiene por completo la disponibilidad del servicio.
2.  **Costos Flexibles pero Elevados:** Los modelos de pago por *token* pueden volverse prohibitivos económicamente al escalar aplicaciones de producción masiva.
3.  **Vulnerabilidad en la Privacidad:** Implica ceder la propiedad intelectual y los datos sensibles del usuario a servidores de terceros bajo sus políticas de privacidad mudables.

**Conclusión personal:**
La ejecución local a través de Ollama es la opción idónea para entornos de desarrollo rápido, prototipado confidencial y aplicaciones que requieran operar al filo de la red (*edge computing*). Sin embargo, para flujos de trabajo empresariales complejos que requieran razonamiento crítico avanzado de nivel superior, el uso híbrido respaldado por APIs en la nube sigue siendo insustituible hoy en día.

---

## 7. Conceptos Clave (Opcional)

**Con base en tu experiencia práctica, explica brevemente:**

### IA vs. Machine Learning vs. Deep Learning
La **IA** es el concepto macro que engloba cualquier sistema capaz de imitar el comportamiento cognitivo humano. El **Machine Learning** es un subcampo de la IA enfocado en algoritmos que aprenden patrones a partir de datos sin ser programados explícitamente. El **Deep Learning** es una especialización del Machine Learning que utiliza redes neuronales artificiales profundas (múltiples capas ocultas) para procesar abstracciones de datos complejas no estructuradas.

### IA Generativa
Es una rama de la Inteligencia Artificial orientada exclusivamente a la creación de contenido nuevo y original (texto, imágenes, código, audio) a partir de patrones aprendidos en grandes bases de datos de entrenamiento, en lugar de limitarse a clasificar o predecir datos existentes.

### Embeddings
Son representaciones matemáticas en forma de vectores de alta dimensionalidad que traducen palabras, frases o conceptos tokens a números. Permiten a las computadoras calcular la similitud semántica y contextual entre diferentes conceptos midiendo la distancia matemática entre sus vectores en un espacio vectorial.

### Transformers
Es la arquitectura de red neuronal que revolucionó el procesamiento de lenguaje natural (NLP). Basada en el mecanismo de "Auto-Atención" (*Self-Attention*), permite al modelo procesar secuencias de datos completas de forma paralela y entender cómo cada palabra se relaciona con todas las demás dentro de una oración, sin importar qué tan alejadas estén.

### Large Language Models (LLM)
Son modelos de IA basados en la arquitectura Transformer, entrenados con volúmenes masivos de datos textuales a escalas multimillonarias de parámetros. Su propósito es comprender, predecir, traducir y generar texto coherente con una estructura y contexto muy similares a los humanos.

---

## 8. Reflexión Final

**¿Qué fue lo más sorprendente o interesante que descubriste en esta práctica?**

**Respuesta:**
Lo más sorprendente de la práctica fue atestiguar la increíble democratización tecnológica que representa **Ollama**. La posibilidad de ejecutar localmente un modelo de apenas 2 o 3 mil millones de parámetros (como Gemma 2 o Llama 3.2) y obtener respuestas con un nivel de estructuración y asimilación semántica tan pulido en español era algo impensable para una computadora personal hace un par de años. 

Ver cómo la optimización a través de la cuantización permite que la lógica computacional corra de forma local abre un abanico inmenso de posibilidades para el desarrollo de proyectos de ingeniería privados y de bajo coste. Me deja con la inquietud de explorar el despliegue de estos pequeños modelos dentro de sistemas embebidos de hardware o microcontroladores avanzados para dotar de autonomía e inteligencia local a prototipos de robótica.

---

**Fecha de elaboración:** 1 de junio de 2026  
**Autor:** Adrian Bazaldua  
**Curso:** IA Generativa y LLMs - Verano 2026