"""
Prueba guiada de la Práctica 4 (sección 13 de las instrucciones):
"genérico vs especializado".

Envía EL MISMO prompt con los MISMOS parámetros a dos perfiles:
    1. Asistente genérico  (perfil "generico")
    2. Copiloto de robótica (perfil "robotica")

y muestra en la terminal, de forma legible, la respuesta completa y las métricas
reales de cada perfil, para poder capturar la evidencia de ejecución.

No se inventa ningún dato: la respuesta y las métricas provienen del backend
(http://127.0.0.1:8000/chat) y se guardan en docs/assets/practica-4/.

Uso:
    python practicas/practica-4/test_guided_comparison.py
"""

import json
import textwrap
from datetime import datetime
from pathlib import Path

import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"

MODEL = "llama3.2:3b"

PROMPT = (
    "Explicame que es la odometria diferencial y dame un ejemplo "
    "para estudiantes de primer semestre."
)

BASE_PARAMS = {
    "model": MODEL,
    "system_prompt": "",  # vacío => el backend usa el system_prompt del perfil
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 400,   # holgado para no truncar la comparación cualitativa
    "num_ctx": 4096,
    "repeat_penalty": 1.1,
}

TARGETS = [
    ("Asistente generico", "generico"),
    ("Copiloto de robotica movil", "robotica"),
]

OUT_DIR = Path(__file__).resolve().parents[2] / "docs" / "assets" / "practica-4"

SEP = "=" * 78
SUB = "-" * 78


def run_one(profile: str) -> dict:
    payload = dict(BASE_PARAMS)
    payload["message"] = PROMPT
    payload["copilot_profile"] = profile
    payload["conversation_id"] = None

    resp = requests.post(BACKEND_URL, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    m = data["metrics"]

    return {
        "profile": data["copilot_profile"],
        "profile_label": data["copilot_label"],
        "system_prompt_used": data.get("system_prompt_used", ""),
        "prompt": PROMPT,
        "model": data["model"],
        "reply": data["reply"],
        "reply_len_chars": len(data["reply"]),
        "prompt_eval_count": m["prompt_eval_count"],   # tokens de entrada
        "eval_count": m["eval_count"],                 # tokens de salida
        "total_tokens": m["total_tokens"],
        "wall_time_s": round(m["wall_time_s"], 3),     # latencia (backend)
        "tokens_per_second": round(m["tokens_per_second"], 2),
    }


def print_block(idx: int, label: str, row: dict) -> None:
    print(SEP)
    print(f"  PRUEBA {idx}  |  PERFIL: {label}  ({row['profile']})")
    print(SEP)
    print(f"  Prompt: {PROMPT}\n")
    print("  Respuesta del modelo:")
    print(SUB)
    for line in row["reply"].splitlines():
        for wrapped in textwrap.wrap(line, width=74) or [""]:
            print(f"  {wrapped}")
    print(SUB)
    print(
        "  Metricas:"
        f"  tokens_entrada={row['prompt_eval_count']}"
        f"  tokens_salida={row['eval_count']}"
        f"  total={row['total_tokens']}"
        f"  latencia={row['wall_time_s']}s"
        f"  {row['tokens_per_second']} tok/s"
    )
    print()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    print()
    print(SEP)
    print("  PRACTICA 4 - PRUEBA GUIADA: GENERICO vs ESPECIALIZADO (seccion 13)")
    print(f"  Modelo: {MODEL}   Backend: {BACKEND_URL}")
    print(f"  Parametros: temperature={BASE_PARAMS['temperature']} "
          f"top_p={BASE_PARAMS['top_p']} num_predict={BASE_PARAMS['num_predict']}")
    print(SEP)
    print()

    rows = []
    for idx, (label, profile) in enumerate(TARGETS, start=1):
        try:
            row = run_one(profile)
            row["label"] = label
            print_block(idx, label, row)
        except Exception as exc:  # noqa: BLE001
            row = {"profile": profile, "label": label, "error": str(exc)}
            print(f"  ERROR en perfil {profile}: {exc}\n")
        rows.append(row)

    ok = [r for r in rows if "error" not in r]
    if len(ok) == 2:
        g, e = ok[0], ok[1]
        print(SEP)
        print("  RESUMEN COMPARATIVO (metricas reales)")
        print(SEP)
        print(f"  {'metrica':<22}{'generico':>16}{'robotica':>16}")
        print(f"  {'tokens de entrada':<22}{g['prompt_eval_count']:>16}{e['prompt_eval_count']:>16}")
        print(f"  {'tokens de salida':<22}{g['eval_count']:>16}{e['eval_count']:>16}")
        print(f"  {'latencia (s)':<22}{g['wall_time_s']:>16}{e['wall_time_s']:>16}")
        print(f"  {'tokens/s':<22}{g['tokens_per_second']:>16}{e['tokens_per_second']:>16}")
        print(SEP)

    out_path = OUT_DIR / f"guided_comparison_{ts}.json"
    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Guardado: {out_path}\n")


if __name__ == "__main__":
    main()
