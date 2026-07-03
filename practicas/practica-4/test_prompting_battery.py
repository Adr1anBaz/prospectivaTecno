"""
Batería de pruebas para la Práctica 4 (copilotos especializados).

Ejecuta, contra el backend en http://127.0.0.1:8000/chat, un conjunto de prompts
de dominio. Cada prompt se envía dos veces con los MISMOS parámetros de generación:
una con el perfil "generico" y otra con el perfil especializado correspondiente,
para permitir la comparación genérico vs especializado.

Cada corrida usa conversation_id = null (conversación nueva), de modo que no hay
contexto acumulado entre pruebas y la comparación es limpia.

No se inventa ningún dato: se guardan las respuestas y las métricas reales que
devuelve el backend (tokens de salida = eval_count, latencia = wall_time_s, etc.).

Uso:
    python practicas/practica-4/test_prompting_battery.py
"""

import json
import time
from datetime import datetime
from pathlib import Path

import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"

MODEL = "llama3.2:3b"

BASE_PARAMS = {
    "model": MODEL,
    "system_prompt": "",  # vacío => el backend usa el system_prompt del perfil
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 180,
    "num_ctx": 4096,
    "repeat_penalty": 1.1,
}

# Prompts por dominio. Cada uno se corre con "generico" y con el perfil indicado.
PROMPTS = [
    ("docente", "Diseña una actividad de clase para introducir el concepto de sensores a estudiantes de primer semestre de ingenieria."),
    ("docente", "Crea una rubrica para evaluar un reporte de laboratorio de robotica."),
    ("docente", "Redacta tres objetivos de aprendizaje para una unidad sobre control de motores."),
    ("robotica", "Como conecto un sensor ultrasonico HC-SR04 a un microcontrolador?"),
    ("robotica", "Explica la diferencia entre un motor DC y un servomotor para un robot movil."),
    ("robotica", "Que precauciones debo tener al alimentar un driver de motores con una bateria LiPo?"),
    ("programacion", "Escribe una funcion en Python que calcule el promedio de una lista de numeros."),
    ("programacion", "Tengo este error: IndexError: list index out of range. Que significa y como lo corrijo?"),
    ("programacion", "Como leo un archivo CSV en Python y sumo una columna?"),
    ("investigacion", "Ayudame a formular una pregunta de investigacion sobre el uso de robots educativos en primaria."),
    ("investigacion", "Que elementos debe tener un marco teorico para un proyecto de vision por computadora?"),
    ("investigacion", "Dame una cita textual con autor y anio de un articulo cientifico sobre aprendizaje basado en proyectos."),
]

OUT_DIR = Path(__file__).resolve().parents[2] / "docs" / "assets" / "practica-4"


def run_one(profile: str, prompt: str) -> dict:
    payload = dict(BASE_PARAMS)
    payload["message"] = prompt
    payload["copilot_profile"] = profile
    payload["conversation_id"] = None

    resp = requests.post(BACKEND_URL, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    m = data["metrics"]

    return {
        "profile": data["copilot_profile"],
        "profile_label": data["copilot_label"],
        "prompt": prompt,
        "model": data["model"],
        "reply": data["reply"],
        "reply_len_chars": len(data["reply"]),
        "eval_count": m["eval_count"],            # tokens de salida
        "prompt_eval_count": m["prompt_eval_count"],  # tokens de entrada
        "total_tokens": m["total_tokens"],
        "wall_time_s": round(m["wall_time_s"], 3),    # latencia (backend)
        "total_duration_s": round(m["total_duration_s"], 3),
        "load_duration_s": round(m["load_duration_s"], 3),
        "eval_duration_s": round(m["eval_duration_s"], 3),
        "tokens_per_second": round(m["tokens_per_second"], 2),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    rows = []
    run_id = 0
    total_runs = len(PROMPTS) * 2

    print(f"Batería Práctica 4 | modelo={MODEL} | corridas={total_runs}")
    print(f"Backend: {BACKEND_URL}\n")

    for specialized, prompt in PROMPTS:
        for profile in ("generico", specialized):
            run_id += 1
            print(f"[{run_id:>2}/{total_runs}] perfil={profile:<13} prompt={prompt[:48]}...")
            try:
                row = run_one(profile, prompt)
            except Exception as exc:  # noqa: BLE001
                print(f"     ERROR: {exc}")
                row = {
                    "profile": profile,
                    "prompt": prompt,
                    "error": str(exc),
                }
            row["run_id"] = run_id
            row["compared_specialized"] = specialized
            rows.append(row)
            time.sleep(0.3)

    raw_path = OUT_DIR / f"metrics_raw_{ts}.json"
    raw_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # Resumen agregado por perfil (solo corridas exitosas)
    ok = [r for r in rows if "error" not in r]
    summary = {}
    for r in ok:
        p = r["profile"]
        summary.setdefault(p, {"runs": 0, "eval_count": 0, "wall_time_s": 0.0, "tokens_per_second": 0.0})
        summary[p]["runs"] += 1
        summary[p]["eval_count"] += r["eval_count"]
        summary[p]["wall_time_s"] += r["wall_time_s"]
        summary[p]["tokens_per_second"] += r["tokens_per_second"]

    for p, s in summary.items():
        n = s["runs"]
        s["avg_eval_count"] = round(s["eval_count"] / n, 1)
        s["avg_wall_time_s"] = round(s["wall_time_s"] / n, 3)
        s["avg_tokens_per_second"] = round(s["tokens_per_second"] / n, 2)

    summary_path = OUT_DIR / f"metrics_summary_{ts}.json"
    summary_path.write_text(
        json.dumps(
            {"model": MODEL, "params": BASE_PARAMS, "n_runs": len(ok), "by_profile": summary},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\nResumen por perfil (promedios):")
    print(f"{'perfil':<14}{'runs':>5}{'tok_out':>10}{'lat_s':>9}{'tok/s':>9}")
    for p, s in summary.items():
        print(f"{p:<14}{s['runs']:>5}{s['avg_eval_count']:>10}{s['avg_wall_time_s']:>9}{s['avg_tokens_per_second']:>9}")

    print(f"\nGuardado:\n  {raw_path}\n  {summary_path}")


if __name__ == "__main__":
    main()
