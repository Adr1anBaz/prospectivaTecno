import os
import json
import time
import uuid

import requests
import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt.mecatronica-ibero.mx")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
CMD_TOPIC = os.getenv("CMD_TOPIC", "public/llm-led/cmd")

ALLOWED_ACTIONS = {"on", "off", "none"}

SYSTEM_PROMPT = """
Eres un clasificador de intención para controlar un LED por MQTT.

Tu tarea es decidir si el usuario quiere:
- "on": encender, prender o activar el LED.
- "off": apagar o desactivar el LED.
- "none": no hay una instrucción clara para cambiar el LED.

Reglas:
1. Responde únicamente JSON válido.
2. No escribas texto fuera del JSON.
3. Si el usuario pregunta algo general, responde action = "none".
4. Si el usuario dice "no enciendas", "no prendas" o algo equivalente, responde action = "none".
5. Si el usuario pide explícitamente apagar, responde action = "off".
6. Si el usuario pide explícitamente encender, responde action = "on".
7. confidence debe estar entre 0 y 1.

Formato obligatorio:
{
  "action": "on" | "off" | "none",
  "confidence": número entre 0 y 1,
  "reason": explicación breve en español
}
"""

app = FastAPI(title="LLM LED Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mqtt_client = mqtt.Client(client_id=f"llm-led-agent-{uuid.uuid4().hex[:8]}")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=30)
mqtt_client.loop_start()


class LedRequest(BaseModel):
    prompt: str


def call_ollama(prompt: str) -> tuple[dict, dict]:
    t0 = time.perf_counter()
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {"temperature": 0.0},
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    raw = r.json()
    elapsed = time.perf_counter() - t0
    text = (raw.get("response") or "").strip()
    metrics = {
        "ollama_latency_s": round(elapsed, 4),
        "prompt_tokens": raw.get("prompt_eval_count"),
        "response_tokens": raw.get("eval_count"),
    }
    return text, metrics


def parse_action(text: str) -> tuple[dict | None, str | None]:
    try:
        data = json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return None, "no_json"
        try:
            data = json.loads(text[start : end + 1])
        except Exception:
            return None, "bad_json"
    if not isinstance(data, dict):
        return None, "not_object"
    action = data.get("action")
    if action not in ALLOWED_ACTIONS:
        return None, "invalid_action"
    try:
        conf = float(data.get("confidence", 0))
    except Exception:
        return None, "bad_confidence"
    if not (0.0 <= conf <= 1.0):
        return None, "confidence_out_of_range"
    reason = str(data.get("reason", "")).strip()
    return {"action": action, "confidence": conf, "reason": reason}, None


def publish_mqtt(action: str) -> bool:
    if action not in {"on", "off"}:
        return False
    info = mqtt_client.publish(CMD_TOPIC, action, qos=1)
    info.wait_for_publish(timeout=5)
    return info.is_published()


@app.get("/health")
def health():
    return {"status": "ok", "model": OLLAMA_MODEL, "broker": MQTT_BROKER, "topic": CMD_TOPIC}


@app.post("/led-agent")
def led_agent(req: LedRequest):
    t_start = time.perf_counter()
    raw, ollama_metrics = call_ollama(req.prompt)
    parsed, parse_error = parse_action(raw)

    json_valid = parsed is not None
    architecture_success = False
    mqtt_published = False
    final_action = None
    final_confidence = None
    final_reason = None

    if parsed:
        final_action = parsed["action"]
        final_confidence = parsed["confidence"]
        final_reason = parsed["reason"]
        try:
            mqtt_published = publish_mqtt(final_action)
        except Exception:
            mqtt_published = False
        architecture_success = mqtt_published

    total_latency = round(time.perf_counter() - t_start, 4)
    return {
        "prompt": req.prompt,
        "raw_response": raw,
        "json_valid": json_valid,
        "parse_error": parse_error,
        "action": final_action,
        "confidence": final_confidence,
        "reason": final_reason,
        "mqtt_published": mqtt_published,
        "architecture_success": architecture_success,
        "total_latency_s": total_latency,
        "ollama_latency_s": ollama_metrics["ollama_latency_s"],
        "prompt_tokens": ollama_metrics["prompt_tokens"],
        "response_tokens": ollama_metrics["response_tokens"],
    }