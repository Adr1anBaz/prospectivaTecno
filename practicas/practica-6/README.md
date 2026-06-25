# Práctica 6: Evaluación de arquitectura LLM + MQTT

Clasificador de intención (on/off/none) que publica en MQTT como salida simulada.

## Requisitos

- Python 3.10+
- Ollama con `llama3.2:3b` (`ollama pull llama3.2:3b`)
- Broker MQTT accesible (`mqtt.mecatronica-ibero.mx:1883` por default)

## Instalación

```bash
cd practica-6/llm_led_eval
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn requests paho-mqtt pydantic pandas numpy openpyxl matplotlib scikit-learn
```

## Ejecución

```bash
# Terminal 1: backend
ollama serve &
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: prueba cíclica (110 prompts aleatorios del dataset)
python run_eval.py

# Terminal 3: análisis + gráficas
python analyze.py
```

## Salidas

`../graficas_resultados/`:
- `resultados.csv` — fila por ejecución
- `supervision.xlsx` — instrumento de supervisión humana
- `confusion_matrix.png`, `latencias.png`, `tokens_vs_latency.png`, `success_rates.png`

## Endpoint

`POST /led-agent` body `{"prompt": "enciende el led"}` → JSON con `action`, `confidence`, `reason`, `mqtt_published`, latencias y tokens.