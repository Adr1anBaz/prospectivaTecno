"""
Genera las gráficas de la Práctica 4 a partir de los datos REALES de la batería.

Lee el archivo más reciente docs/assets/practica-4/metrics_raw_*.json (métricas
medidas por el backend) y produce archivos PNG en la misma carpeta. No se inventa
ningún valor: todas las gráficas se calculan a partir de las corridas registradas.

La evaluación cualitativa (¿alucina?) proviene de la lectura de las respuestas
reales y coincide con la tabla de pruebas del reporte docs/practica-4.md.

Uso:
    python practicas/practica-4/graficar.py
"""

import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ASSETS = Path(__file__).resolve().parents[2] / "docs" / "assets" / "practica-4"

ORDER = ["generico", "docente", "robotica", "programacion", "investigacion"]
COLORS = {
    "generico": "#94a3b8",
    "docente": "#2563eb",
    "robotica": "#16a34a",
    "programacion": "#9333ea",
    "investigacion": "#ea580c",
}

# ¿Alucina? por corrida, derivado de la lectura de las respuestas reales
# (mismos valores que la tabla de pruebas de docs/practica-4.md).
HALLUCINATION = {
    "generico":      {"No": 7, "Leve": 4, "Sí": 1},
    "docente":       {"No": 3, "Leve": 0, "Sí": 0},
    "robotica":      {"No": 0, "Leve": 1, "Sí": 2},
    "programacion":  {"No": 3, "Leve": 0, "Sí": 0},
    "investigacion": {"No": 2, "Leve": 0, "Sí": 1},
}

PROMPT_LABELS = [f"P{i}" for i in range(1, 13)]


def latest_raw() -> Path:
    files = sorted(ASSETS.glob("metrics_raw_*.json"))
    if not files:
        raise SystemExit("No se encontró metrics_raw_*.json en docs/assets/practica-4/")
    return files[-1]


def load_rows(path: Path) -> list:
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [r for r in rows if "error" not in r]


def averages(rows: list):
    by = defaultdict(lambda: {"in": 0, "out": 0, "lat": 0.0, "tps": 0.0, "n": 0})
    for r in rows:
        p = r["profile"]
        by[p]["in"] += r["prompt_eval_count"]
        by[p]["out"] += r["eval_count"]
        by[p]["lat"] += r["wall_time_s"]
        by[p]["tps"] += r["tokens_per_second"]
        by[p]["n"] += 1
    profiles = [p for p in ORDER if p in by]
    avg_in = [by[p]["in"] / by[p]["n"] for p in profiles]
    avg_lat = [by[p]["lat"] / by[p]["n"] for p in profiles]
    avg_tps = [by[p]["tps"] / by[p]["n"] for p in profiles]
    return profiles, avg_in, avg_lat, avg_tps


def bar_by_profile(profiles, values, title, ylabel, fname, fmt="{:.0f}"):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = [COLORS.get(p, "#64748b") for p in profiles]
    bars = ax.bar(profiles, values, color=colors)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, max(values) * 1.18)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v, fmt.format(v),
                ha="center", va="bottom", fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = ASSETS / fname
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("  ->", out.name)


def grouped_latency_by_prompt(rows):
    gen = {}
    esp = {}
    esp_profile = {}
    for r in rows:
        key = r["compared_specialized"]
        if r["profile"] == "generico":
            gen[key] = gen.get(key, [])
            gen[key].append(r)
        else:
            esp[key] = r
            esp_profile[key] = r["profile"]

    # Reordenar por perfil especializado para agrupar visualmente
    ordered_keys = []
    seen = []
    # 12 prompts en el orden P1..P12 de la batería: usar run_id para ordenar
    pairs = defaultdict(dict)
    for r in rows:
        pairs[r["run_id"]]  # touch
    # Mapear a P1..P12 según orden de aparición de prompts especializados
    prompts_order = []
    for r in sorted(rows, key=lambda x: x["run_id"]):
        if r["profile"] != "generico":
            prompts_order.append(r["prompt"])
    prompts_order = list(dict.fromkeys(prompts_order))

    gen_by_prompt = {}
    esp_by_prompt = {}
    esp_prof_by_prompt = {}
    for r in rows:
        if r["profile"] == "generico":
            gen_by_prompt[r["prompt"]] = r["wall_time_s"]
        else:
            esp_by_prompt[r["prompt"]] = r["wall_time_s"]
            esp_prof_by_prompt[r["prompt"]] = r["profile"]

    labels = PROMPT_LABELS[:len(prompts_order)]
    gen_vals = [gen_by_prompt.get(p, 0) for p in prompts_order]
    esp_vals = [esp_by_prompt.get(p, 0) for p in prompts_order]

    fig, ax = plt.subplots(figsize=(11, 4.8))
    x = range(len(labels))
    w = 0.4
    ax.bar([i - w / 2 for i in x], gen_vals, width=w, label="genérico", color="#94a3b8")
    ax.bar([i + w / 2 for i in x], esp_vals, width=w, label="especializado", color="#2563eb")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("latencia (s)")
    ax.set_title("Latencia por prompt: genérico vs especializado (llama3.2:3b)",
                 fontsize=13, fontweight="bold")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = ASSETS / "latencia_generico_vs_especializado.png"
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("  ->", out.name)


def output_tokens_per_run(rows):
    ordered = sorted(rows, key=lambda x: x["run_id"])
    vals = [r["eval_count"] for r in ordered]
    colors = [COLORS.get(r["profile"], "#64748b") for r in ordered]
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.bar(range(len(vals)), vals, color=colors)
    ax.axhline(180, color="#dc2626", linestyle="--", linewidth=1,
               label="tope num_predict = 180")
    ax.set_xlabel("corrida (run_id)")
    ax.set_ylabel("tokens de salida (eval_count)")
    ax.set_title("Tokens de salida por corrida (24 corridas)",
                 fontsize=13, fontweight="bold")
    ax.set_ylim(0, 200)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    from matplotlib.patches import Patch
    handles = [Patch(color=COLORS[p], label=p) for p in ORDER]
    handles.append(Patch(color="#dc2626", label="tope 180"))
    ax.legend(handles=handles, fontsize=8, ncol=3)
    fig.tight_layout()
    out = ASSETS / "tokens_salida_por_corrida.png"
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("  ->", out.name)


def hallucination_chart():
    profiles = ORDER
    levels = ["No", "Leve", "Sí"]
    level_colors = {"No": "#16a34a", "Leve": "#f59e0b", "Sí": "#dc2626"}
    fig, ax = plt.subplots(figsize=(9, 4.8))
    bottoms = [0] * len(profiles)
    for lvl in levels:
        vals = [HALLUCINATION[p][lvl] for p in profiles]
        ax.bar(profiles, vals, bottom=bottoms, label=lvl, color=level_colors[lvl])
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax.set_ylabel("número de corridas")
    ax.set_title("Evaluación cualitativa: ¿alucina? por perfil\n(lectura de las respuestas reales)",
                 fontsize=12, fontweight="bold")
    ax.legend(title="¿Alucina?")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = ASSETS / "evaluacion_alucinaciones.png"
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("  ->", out.name)


def main():
    raw = latest_raw()
    print(f"Datos: {raw.name}")
    rows = load_rows(raw)
    print(f"Corridas válidas: {len(rows)}\n")
    print("Generando gráficas:")

    profiles, avg_in, avg_lat, avg_tps = averages(rows)
    bar_by_profile(profiles, avg_in,
                   "Tokens de entrada promedio por perfil\n(costo del system_prompt)",
                   "tokens de entrada (prom.)", "tokens_entrada_por_perfil.png",
                   fmt="{:.0f}")
    bar_by_profile(profiles, avg_lat,
                   "Latencia promedio por perfil (llama3.2:3b)",
                   "latencia (s, prom.)", "latencia_por_perfil.png", fmt="{:.2f}")
    bar_by_profile(profiles, avg_tps,
                   "Rendimiento promedio por perfil",
                   "tokens/s (prom.)", "tokens_por_segundo_por_perfil.png", fmt="{:.1f}")
    grouped_latency_by_prompt(rows)
    output_tokens_per_run(rows)
    hallucination_chart()

    print(f"\nGráficas guardadas en: {ASSETS}")


if __name__ == "__main__":
    main()
