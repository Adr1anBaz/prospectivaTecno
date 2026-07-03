"""
Batería de pruebas para la Práctica 5 (chatbot híbrido con APIs externas).

Envía, contra el backend en http://127.0.0.1:8000/chat, EL MISMO prompt y los MISMOS
parámetros de generación a tres proveedores, N veces cada uno, para poder promediar
las métricas de inferencia y comparar el modelo local con los remotos.

Proveedores evaluados (según la sección 14 de las instrucciones):
    1. Ollama local        -> llama3.2:3b
    2. Gemini (vía OpenRouter) -> google/gemini-2.5-flash-lite
    3. Groq API            -> llama-3.3-70b-versatile

Nota: no se dispone de una GEMINI_API_KEY directa de Google, por lo que la columna
"Gemini" se cubre usando Gemini a través de OpenRouter (google/gemini-2.5-flash-lite).

No se inventa ningún dato: se guardan las respuestas y las métricas reales que devuelve
el backend (wall_time_s, prompt_tokens, completion_tokens, total_tokens, tokens_per_second).

Uso:
    python practicas/practica-5/test_hybrid_battery.py
"""

import json
import time
from datetime import datetime
from pathlib import Path

import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"

N_REPS = 3

PROMPT = (
    "Explica qué es la odometría diferencial en un robot móvil de dos ruedas.\n"
    "Incluye:\n"
    "1. explicación conceptual;\n"
    "2. ecuaciones básicas;\n"
    "3. ejemplo para estudiantes de ingeniería;\n"
    "4. una limitación práctica.\n"
    "Responde en máximo 250 palabras."
)

BASE_PARAMS = {
    "copilot_profile": "robotica",
    "system_prompt": "",  # vacío => el backend usa el system_prompt del perfil
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 300,
    "num_ctx": 4096,
    "repeat_penalty": 1.1,
}

# (etiqueta_para_reporte, provider, model)
TARGETS = [
    ("Ollama local", "ollama", "llama3.2:3b"),
    ("Gemini (OpenRouter)", "openrouter", "google/gemini-2.5-flash-lite"),
    ("Groq API", "groq", "llama-3.3-70b-versatile"),
]

OUT_DIR = Path(__file__).resolve().parents[2] / "docs" / "assets" / "practica-5"


def run_one(provider: str, model: str) -> dict:
    payload = dict(BASE_PARAMS)
    payload["message"] = PROMPT
    payload["provider"] = provider
    payload["model"] = model

    resp = requests.post(BACKEND_URL, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    m = data["metrics"]

    return {
        "provider": data["provider"],
        "model": data["model"],
        "copilot_label": data["copilot_label"],
        "reply": data["reply"],
        "reply_len_chars": len(data["reply"]),
        "wall_time_s": round(m["wall_time_s"], 3),
        "provider_duration_s": round(m["provider_duration_s"], 3),
        "prompt_tokens": m["prompt_tokens"],
        "completion_tokens": m["completion_tokens"],
        "total_tokens": m["total_tokens"],
        "tokens_per_second": round(m["tokens_per_second"], 2),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    total_runs = len(TARGETS) * N_REPS
    print(f"Batería Práctica 5 | proveedores={len(TARGETS)} | reps={N_REPS} | corridas={total_runs}")
    print(f"Backend: {BACKEND_URL}\n")

    rows = []
    run_id = 0
    for label, provider, model in TARGETS:
        for rep in range(1, N_REPS + 1):
            run_id += 1
            print(f"[{run_id:>2}/{total_runs}] {label:<22} rep {rep}/{N_REPS} ...", end=" ", flush=True)
            try:
                row = run_one(provider, model)
                print(
                    f"in={row['prompt_tokens']} out={row['completion_tokens']} "
                    f"{row['wall_time_s']}s {row['tokens_per_second']} tok/s"
                )
            except Exception as exc:  # noqa: BLE001
                print(f"ERROR: {exc}")
                row = {"provider": provider, "model": model, "error": str(exc)}
            row["label"] = label
            row["rep"] = rep
            row["run_id"] = run_id
            rows.append(row)
            time.sleep(0.4)

    raw_path = OUT_DIR / f"metrics_raw_{ts}.json"
    raw_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # Resumen agregado por proveedor (solo corridas exitosas)
    ok = [r for r in rows if "error" not in r]
    summary = {}
    for r in ok:
        key = r["label"]
        s = summary.setdefault(
            key,
            {
                "provider": r["provider"],
                "model": r["model"],
                "runs": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "wall_time_s": 0.0,
                "tokens_per_second": 0.0,
            },
        )
        s["runs"] += 1
        s["prompt_tokens"] += r["prompt_tokens"]
        s["completion_tokens"] += r["completion_tokens"]
        s["total_tokens"] += r["total_tokens"]
        s["wall_time_s"] += r["wall_time_s"]
        s["tokens_per_second"] += r["tokens_per_second"]

    for s in summary.values():
        n = s["runs"]
        s["avg_prompt_tokens"] = round(s["prompt_tokens"] / n, 1)
        s["avg_completion_tokens"] = round(s["completion_tokens"] / n, 1)
        s["avg_total_tokens"] = round(s["total_tokens"] / n, 1)
        s["avg_wall_time_s"] = round(s["wall_time_s"] / n, 3)
        s["avg_tokens_per_second"] = round(s["tokens_per_second"] / n, 2)

    summary_path = OUT_DIR / f"metrics_summary_{ts}.json"
    summary_path.write_text(
        json.dumps(
            {
                "prompt": PROMPT,
                "params": BASE_PARAMS,
                "n_reps": N_REPS,
                "n_runs_ok": len(ok),
                "by_provider": summary,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\nResumen por proveedor (promedios):")
    print(f"{'proveedor':<22}{'runs':>5}{'tok_in':>8}{'tok_out':>9}{'lat_s':>9}{'tok/s':>9}")
    for label, s in summary.items():
        print(
            f"{label:<22}{s['runs']:>5}{s['avg_prompt_tokens']:>8}"
            f"{s['avg_completion_tokens']:>9}{s['avg_wall_time_s']:>9}{s['avg_tokens_per_second']:>9}"
        )

    print(f"\nGuardado:\n  {raw_path}\n  {summary_path}")


if __name__ == "__main__":
    main()
