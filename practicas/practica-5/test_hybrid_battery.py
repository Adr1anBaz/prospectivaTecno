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

from __future__ import annotations

import json
import math
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

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
    "system_prompt": "",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 300,
    "num_ctx": 4096,
    "repeat_penalty": 1.1,
}

TARGETS: List[Tuple[str, str, str]] = [
    ("Ollama local",            "ollama",     "llama3.2:3b"),
    ("Gemini (OpenRouter)",     "openrouter", "google/gemini-2.5-flash-lite"),
    ("Groq API",                "groq",       "llama-3.3-70b-versatile"),
]

OUT_DIR = Path(__file__).resolve().parents[2] / "docs" / "assets" / "practica-5"
CHART_DIR = Path(__file__).resolve().parents[2] / "docs" / "imgs" / "pr5"

# ── ANSI helpers ──────────────────────────────────────────────────────────────
class styl:
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RST = "\033[0m"
    RED = "\033[91m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    BLU = "\033[94m"
    MAG = "\033[95m"
    CYN = "\033[96m"
    LRED = "\033[101m"
    LGRN = "\033[102m"

PASS = f"{styl.GRN}✓{styl.RST}"
FAIL = f"{styl.RED}✗{styl.RST}"

ICONS = {
    "Ollama local": "🖥",
    "Gemini (OpenRouter)": "🌀",
    "Groq API": "⚡",
}

def bar(pct: float, width: int = 20) -> str:
    filled = math.floor(pct * width)
    return "[" + "█" * filled + "░" * (width - filled) + "]"


# ── Core ─────────────────────────────────────────────────────────────────────
def run_one(provider: str, model: str) -> dict:
    payload = dict(BASE_PARAMS)
    payload["message"] = PROMPT
    payload["provider"] = provider
    payload["model"] = model

    t0 = time.perf_counter()
    resp = requests.post(BACKEND_URL, json=payload, timeout=300)
    t1 = time.perf_counter()
    resp.raise_for_status()
    data = resp.json()
    m = data["metrics"]

    return {
        "provider": data["provider"],
        "model": data["model"],
        "copilot_label": data["copilot_label"],
        "reply": data["reply"],
        "reply_len_chars": len(data["reply"]),
        "http_elapsed_s": round(t1 - t0, 4),
        "wall_time_s": round(m["wall_time_s"], 4),
        "provider_duration_s": round(m["provider_duration_s"], 4),
        "prompt_tokens": m["prompt_tokens"],
        "completion_tokens": m["completion_tokens"],
        "total_tokens": m["total_tokens"],
        "tokens_per_second": round(m["tokens_per_second"], 2),
    }


def print_run(label: str, rep: int, run_id: int, total: int, row: dict) -> None:
    ok = "error" not in row
    status = PASS if ok else FAIL
    icon = ICONS.get(label, "?")
    pct = run_id / total

    line = (
        f"  {bar(pct)} {styl.BOLD}{run_id:>2}/{total}{styl.RST} "
        f"{icon} {styl.CYN}{label:<22}{styl.RST} "
        f"{styl.DIM}rep{rep}{styl.RST} "
        f"{status} "
    )

    if ok:
        tok_s = row["tokens_per_second"]
        tok_s_str = f"{styl.GRN}{tok_s:>7.2f}{styl.RST} tok/s" if tok_s > 100 else f"{tok_s:>7.2f} tok/s"
        line += (
            f"│ "
            f"{styl.BOLD}in{styl.RST}={row['prompt_tokens']:<4} "
            f"{styl.BOLD}out{styl.RST}={row['completion_tokens']:<4} "
            f"{styl.BOLD}tot{styl.RST}={row['total_tokens']:<4} "
            f"│ "
            f"{styl.YLW}{row['wall_time_s']:>6.3f}s{styl.RST} "
            f"│ "
            f"{tok_s_str}"
        )
    else:
        line += f"{styl.RED}{row.get('error', 'unknown error')}{styl.RST}"

    print(line)


def print_provider_header(label: str, idx: int, total_providers: int) -> None:
    icon = ICONS.get(label, "?")
    sep = f"{styl.MAG}{'═' * 74}{styl.RST}"
    print(f"\n{sep}")
    print(
        f"  {styl.BOLD}{styl.BLU}[{idx}/{total_providers}]{styl.RST} "
        f"{icon} {styl.BOLD}{label}{styl.RST}"
    )
    print(f"  {styl.DIM}{'─' * 50}{styl.RST}")


def compute_stats(values: List[float]) -> Dict[str, float]:
    if not values:
        return {}
    return {
        "mean": round(statistics.fmean(values), 3),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
        "stdev": round(statistics.pstdev(values), 3) if len(values) > 1 else 0.0,
    }


def generate_charts(summary: dict) -> None:
    if not HAS_MPL:
        print(f"  {styl.DIM}[charts] matplotlib no disponible — omitiendo gráficas{styl.RST}")
        return

    if not summary:
        print(f"  {styl.DIM}[charts] no hay datos — omitiendo gráficas{styl.RST}")
        return

    CHART_DIR.mkdir(parents=True, exist_ok=True)
    providers_data = list(summary.items())

    labels = [p[0] for p in providers_data]
    short_labels = [l.split("(")[0].strip()[:16] for l in labels]

    def val(key):
        return [p[1].get(key, 0) for p in providers_data]

    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
    })

    colors = ["steelblue", "seagreen", "darkorange"]

    # ── Chart 1: Wall time ──
    fig, ax = plt.subplots(figsize=(8, 5))
    wt = val("avg_wall_time_s")
    bars = ax.bar(range(len(labels)), wt, color=colors[:len(labels)], edgecolor="black")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(short_labels, fontsize=10)
    ax.set_ylabel("Tiempo (s)")
    ax.set_title("Tiempo de Respuesta por Proveedor (promedio)")
    ax.grid(axis="y", alpha=0.3)
    for bar, v in zip(bars, wt):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{v:.3f}s", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "chart_wall_time.png", dpi=200)
    plt.close(fig)

    # ── Chart 2: Tokens/s ──
    fig, ax = plt.subplots(figsize=(8, 5))
    tps = val("avg_tokens_per_second")
    bars = ax.bar(range(len(labels)), tps, color=colors[:len(labels)], edgecolor="black")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(short_labels, fontsize=10)
    ax.set_ylabel("Tokens/s")
    ax.set_title("Velocidad de Generación por Proveedor (promedio)")
    ax.grid(axis="y", alpha=0.3)
    for bar, v in zip(bars, tps):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{v:.1f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "chart_tokens_per_second.png", dpi=200)
    plt.close(fig)

    # ── Chart 3: Prompt vs Completion ──
    fig, ax = plt.subplots(figsize=(8, 5))
    w = 0.3
    x = range(len(labels))
    pt = val("avg_prompt_tokens")
    ct = val("avg_completion_tokens")
    bars1 = ax.bar([i - w / 2 for i in x], pt, w, label="Prompt (entrada)", color="coral", edgecolor="darkred")
    bars2 = ax.bar([i + w / 2 for i in x], ct, w, label="Completion (salida)", color="goldenrod", edgecolor="darkgoldenrod")
    ax.set_xticks(list(x))
    ax.set_xticklabels(short_labels, fontsize=10)
    ax.set_ylabel("Tokens")
    ax.set_title("Tokens de Entrada vs Salida por Proveedor")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 2, f"{int(h)}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "chart_prompt_vs_completion.png", dpi=200)
    plt.close(fig)

    # ── Chart 4: Latency vs Speed ──
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax2 = ax1.twinx()
    x = range(len(labels))
    bars = ax1.bar(x, wt, color=colors[:len(labels)], edgecolor="black", alpha=0.7, label="Wall time (s)")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(short_labels, fontsize=10)
    ax1.set_ylabel("Tiempo (s)")
    ax1.set_title("Comparativa General: Latencia vs Velocidad")
    line = ax2.plot(x, tps, "D-", color="crimson", linewidth=2.5, markersize=8, label="Tokens/s")
    ax2.set_ylabel("Tokens/s")
    for i, v in enumerate(tps):
        ax2.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, 10),
                     ha="center", fontsize=9, color="crimson", fontweight="bold")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)
    ax1.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "chart_latency_vs_speed.png", dpi=200)
    plt.close(fig)

    print(f"  {styl.DIM}[charts] gráficas guardadas en {CHART_DIR}/{styl.RST}")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    total_runs = len(TARGETS) * N_REPS
    n_providers = len(TARGETS)

    # ── Banner ──────────────────────────────────────────────────────────
    print()
    print(f"  {styl.BOLD}{styl.BLU}{'╔' + '═' * 72 + '╗'}{styl.RST}")
    print(f"  {styl.BOLD}{styl.BLU}║{styl.RST}  {styl.BOLD}{styl.CYN}BATERÍA DE PRUEBAS — PRÁCTICA 5{styl.RST}{' ' * 31}{styl.BOLD}{styl.BLU}║{styl.RST}")
    print(f"  {styl.BOLD}{styl.BLU}║{styl.RST}  {styl.DIM}Chatbot híbrido: Ollama + Groq + OpenRouter{styl.RST}{' ' * 14}{styl.BOLD}{styl.BLU}║{styl.RST}")
    print(f"  {styl.BOLD}{styl.BLU}╚{'═' * 72 + '╝'}{styl.RST}")
    print()
    print(f"    {styl.BOLD}Endpoint:{styl.RST}   {BACKEND_URL}")
    print(f"    {styl.BOLD}Proveedores:{styl.RST} {n_providers}  {styl.BOLD}Repeticiones:{styl.RST} {N_REPS}  {styl.BOLD}Total corridas:{styl.RST} {total_runs}")
    print(f"    {styl.BOLD}Prompt:{styl.RST}     {PROMPT[:60]}...")
    print()

    rows: List[Dict[str, Any]] = []
    run_id = 0

    t_battery_start = time.perf_counter()

    for p_idx, (label, provider, model) in enumerate(TARGETS, 1):
        print_provider_header(label, p_idx, n_providers)

        for rep in range(1, N_REPS + 1):
            run_id += 1
            try:
                row = run_one(provider, model)
            except Exception as exc:
                row = {"provider": provider, "model": model, "error": str(exc)}

            row["label"] = label
            row["rep"] = rep
            row["run_id"] = run_id
            rows.append(row)
            print_run(label, rep, run_id, total_runs, row)

            if rep < N_REPS:
                time.sleep(0.3)

    t_battery_end = time.perf_counter()
    battery_elapsed = t_battery_end - t_battery_start

    # ── Save raw ────────────────────────────────────────────────────────
    raw_path = OUT_DIR / f"metrics_raw_{ts}.json"
    raw_path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ── Aggregate ───────────────────────────────────────────────────────
    ok_rows = [r for r in rows if "error" not in r]
    failed_rows = [r for r in rows if "error" in r]

    summary: Dict[str, Any] = {}
    for r in ok_rows:
        key = r["label"]
        s = summary.setdefault(key, {
            "provider": r["provider"],
            "model": r["model"],
            "runs": 0,
            "wall_time_s": [],
            "tokens_per_second": [],
            "prompt_tokens": [],
            "completion_tokens": [],
            "total_tokens": [],
            "reply_len_chars": [],
        })
        s["runs"] += 1
        s["wall_time_s"].append(r["wall_time_s"])
        s["tokens_per_second"].append(r["tokens_per_second"])
        s["prompt_tokens"].append(r["prompt_tokens"])
        s["completion_tokens"].append(r["completion_tokens"])
        s["total_tokens"].append(r["total_tokens"])
        s["reply_len_chars"].append(r["reply_len_chars"])

    # Compute averages + stats
    for s in summary.values():
        s["avg_wall_time_s"] = round(statistics.fmean(s["wall_time_s"]), 3)
        s["avg_tokens_per_second"] = round(statistics.fmean(s["tokens_per_second"]), 2)
        s["avg_prompt_tokens"] = round(statistics.fmean(s["prompt_tokens"]), 1)
        s["avg_completion_tokens"] = round(statistics.fmean(s["completion_tokens"]), 1)
        s["avg_total_tokens"] = round(statistics.fmean(s["total_tokens"]), 1)

    summary_path = OUT_DIR / f"metrics_summary_{ts}.json"
    summary_path.write_text(
        json.dumps({
            "prompt": PROMPT,
            "params": BASE_PARAMS,
            "n_reps": N_REPS,
            "n_runs_total": len(rows),
            "n_runs_ok": len(ok_rows),
            "n_runs_failed": len(failed_rows),
            "battery_elapsed_s": round(battery_elapsed, 2),
            "by_provider": {
                k: {kk: vv for kk, vv in s.items() if kk != "reply_len_chars"}
                for k, s in summary.items()
            },
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # ── Summary table ───────────────────────────────────────────────────
    sep_double = f"  {styl.BOLD}{styl.BLU}{'═' * 74}{styl.RST}"
    sep_single = f"  {styl.DIM}{'─' * 74}{styl.RST}"

    print(f"\n{sep_double}")
    print(f"  {styl.BOLD}{styl.CYN}📊  RESUMEN AGREGADO POR PROVEEDOR{styl.RST}")
    print(sep_single)

    header = (
        f"  {styl.BOLD}{'PROVEEDOR':<24} {'RUNS':>5} {'TOK_IN':>8} {'TOK_OUT':>9} "
        f"{'TOTAL':>7} {'LATENCIA':>10} {'TOK/S':>8}  {'RANK':>5}{styl.RST}"
    )
    print(header)
    print(sep_single)

    # Sort by avg_tokens_per_second descending
    sorted_providers = sorted(summary.items(), key=lambda x: x[1]["avg_tokens_per_second"], reverse=True)
    for rank, (label, s) in enumerate(sorted_providers, 1):
        rank_badge = f"{styl.GRN}🥇{styl.RST}" if rank == 1 else f"{styl.YLW}🥈{styl.RST}" if rank == 2 else f"{styl.DIM}🥉{styl.RST}" if rank == 3 else f" #{rank} "
        icon = ICONS.get(label, " ")
        print(
            f"  {icon} {label:<22} "
            f"{s['runs']:>5} "
            f"{s['avg_prompt_tokens']:>8.0f} "
            f"{s['avg_completion_tokens']:>9.0f} "
            f"{s['avg_total_tokens']:>7.0f} "
            f"{styl.YLW}{s['avg_wall_time_s']:>8.3f}s{styl.RST} "
            f"{styl.GRN if rank == 1 else ''}{s['avg_tokens_per_second']:>8.2f}{styl.RST} "
            f" {rank_badge}"
        )

    print(sep_double)

    # ── Statistical detail ──────────────────────────────────────────────
    print(f"\n  {styl.BOLD}{styl.CYN}📈  DESGLOSE ESTADÍSTICO POR MÉTRICA{styl.RST}\n")

    metrics_config = [
        ("wall_time_s",       "Wall time (s)",     "{:.3f}",   "s"),
        ("tokens_per_second", "Tokens/s",          "{:.2f}",   ""),
        ("prompt_tokens",     "Prompt tokens",     "{:.0f}",   " tok"),
        ("completion_tokens", "Completion tokens",  "{:.0f}",   " tok"),
        ("total_tokens",      "Total tokens",      "{:.0f}",   " tok"),
    ]

    for field, display_name, fmt, unit in metrics_config:
        print(f"  {styl.BOLD}{display_name}{styl.RST}")
        for label, s in summary.items():
            vals = s.get(field, [])
            if not vals:
                continue
            stats = compute_stats(vals)
            icon = ICONS.get(label, " ")
            print(
                f"    {icon} {label:<24} "
                f"{styl.DIM}μ={fmt.format(stats['mean'])}{unit}{styl.RST}  "
                f"{styl.DIM}min={fmt.format(stats['min'])}{unit}{styl.RST}  "
                f"{styl.DIM}max={fmt.format(stats['max'])}{unit}{styl.RST}  "
                f"{styl.DIM}σ={fmt.format(stats['stdev'])}{unit}{styl.RST}"
            )
        print()

    # ── Battery summary ─────────────────────────────────────────────────
    print(f"  {styl.BOLD}{styl.BLU}{'═' * 74}{styl.RST}")
    print(f"  {styl.BOLD}{styl.CYN}⚡  CIERRE DE BATERÍA{styl.RST}")
    print(f"  {styl.DIM}{'─' * 50}{styl.RST}")

    ok_count = len(ok_rows)
    fail_count = len(failed_rows)
    status_icon = PASS if fail_count == 0 else FAIL

    print(f"    {status_icon}  Total corridas:  {styl.BOLD}{len(rows)}{styl.RST}  "
          f"({styl.GRN}{ok_count} ok{styl.RST}  "
          f"{styl.RED}{fail_count} failed{styl.RST})")
    print(f"    ⏱  Tiempo total:   {styl.YLW}{battery_elapsed:.1f}s{styl.RST}  "
          f"({battery_elapsed / 60:.1f} min)")
    print(f"    📁 Raw JSON:      {styl.DIM}{raw_path}{styl.RST}")
    print(f"    📁 Summary JSON:  {styl.DIM}{summary_path}{styl.RST}")
    print(f"  {styl.BOLD}{styl.BLU}{'═' * 74}{styl.RST}")
    print()

    generate_charts(summary)

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
