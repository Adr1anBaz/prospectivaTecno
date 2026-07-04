#!/usr/bin/env python3
"""
Batería de pruebas para la práctica 3 (chatbot con contexto en SQLite).

Manda N peticiones al endpoint /chat del backend por cada escenario,
captura métricas y agrega resultados (mean / median / min / max / stdev).
Solo usa Ollama local. El backend debe estar corriendo en BACKEND_URL.

Estrategia de contexto (S2, S8):
    Para poblar el historial hacemos POST /chat reales previos usando el
    conversation_id de SQLite. Solo la ÚLTIMA llamada del run se mide; las
    llamadas de seed descartan sus métricas.
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

BACKEND_URL = "http://127.0.0.1:8000/chat"
RUNS_PER_SCENARIO = 5
TIMEOUT_S = 180
MODEL = "llama3.2:3b"
RUN_TAG = time.strftime("%Y%m%d_%H%M%S")
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "assets" / "practica-3"
CHART_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "imgs" / "pr3"
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


# Este backend usa num_predict (no max_tokens).
BASE_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 160,
    "num_ctx": 4096,
    "repeat_penalty": 1.1,
}


def post_chat(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        r = requests.post(BACKEND_URL, json=payload, timeout=TIMEOUT_S)
    except requests.exceptions.RequestException as exc:
        return {"_error": f"{type(exc).__name__}: {exc}"}

    try:
        data = r.json()
    except ValueError:
        return {"_error": f"HTTP {r.status_code}: respuesta no JSON"}

    if r.status_code != 200:
        return {"_error": f"HTTP {r.status_code}: {data.get('detail', data)}"}

    return data


def build_scenarios() -> List[Dict[str, Any]]:
    """Cada escenario se ejecuta RUNS_PER_SCENARIO veces."""
    return [
        {
            "id": "S1",
            "name": "Primer mensaje (sin historial)",
            "description": "Conversacion nueva, pregunta conceptual breve.",
            "run": lambda i: {
                **BASE_PARAMS,
                "message": "Explica brevemente que es Python.",
            },
        },
        {
            "id": "S2",
            "name": "Tercer mensaje (historial corto)",
            "description": "Sembrar 2 turnos previos y mandar el tercero (seed via POST reales).",
            "setup": "seed_history_short",
            "user_message": "Cual de esos es mejor para comenzar?",
            "run_params": BASE_PARAMS,
        },
        {
            "id": "S3",
            "name": "Respuesta tecnica",
            "description": "Pedir ejemplo de codigo con salida larga.",
            "run": lambda i: {
                **BASE_PARAMS,
                "num_predict": 400,
                "message": "Dame un ejemplo de codigo en Python que use FastAPI y SQLAlchemy.",
            },
        },
        {
            "id": "S4",
            "name": "Temperatura baja (0.2)",
            "description": "Mismo prompt que S1, temperature=0.2.",
            "run": lambda i: {
                **BASE_PARAMS,
                "temperature": 0.2,
                "message": "Explica brevemente que es Python.",
            },
        },
        {
            "id": "S5",
            "name": "Temperatura alta (1.0)",
            "description": "Mismo prompt que S1, temperature=1.0.",
            "run": lambda i: {
                **BASE_PARAMS,
                "temperature": 1.0,
                "message": "Explica brevemente que es Python.",
            },
        },
        {
            "id": "S6",
            "name": "num_predict corto (60)",
            "description": "Mismo prompt que S1, salida limitada a 60 tokens.",
            "run": lambda i: {
                **BASE_PARAMS,
                "num_predict": 60,
                "message": "Explica brevemente que es Python.",
            },
        },
        {
            "id": "S7",
            "name": "num_predict largo (300)",
            "description": "Mismo prompt que S1, salida hasta 300 tokens.",
            "run": lambda i: {
                **BASE_PARAMS,
                "num_predict": 300,
                "message": "Explica brevemente que es Python.",
            },
        },
        {
            "id": "S8",
            "name": "Historial largo (10 turnos)",
            "description": "Sembrar 9 turnos previos y mandar el decimo (seed via POST reales).",
            "setup": "seed_history_long",
            "user_message": "Resumi lo que hemos cubierto hasta ahora.",
            "run_params": BASE_PARAMS,
        },
    ]


def seed_history_short() -> List[Dict[str, str]]:
    return [
        {"role": "user", "content": "Me llamo Adrian y estudio ingenieria."},
        {"role": "assistant", "content": "Hola Adrian, en que puedo ayudarte hoy?"},
        {"role": "user", "content": "Que lenguajes de programacion deberia aprender?"},
        {"role": "assistant", "content": "Para ingenieria te recomiendo Python, C y JavaScript como base."},
    ]


def seed_history_long() -> List[Dict[str, str]]:
    base = seed_history_short()
    base += [
        {"role": "user", "content": "Que es Python en particular?"},
        {"role": "assistant", "content": "Python es un lenguaje interpretado, multiparadigma y de alto nivel."},
        {"role": "user", "content": "Y para que se usa comunmente?"},
        {"role": "assistant", "content": "Se usa en web, datos, IA, scripting, automatizacion y prototipado."},
        {"role": "user", "content": "Cual es su ventaja principal?"},
        {"role": "assistant", "content": "Su legibilidad y ecosistema de librerias."},
        {"role": "user", "content": "Que framework web me recomiendas?"},
        {"role": "assistant", "content": "FastAPI y Django son los mas usados en produccion."},
        {"role": "user", "content": "Y para ciencia de datos?"},
        {"role": "assistant", "content": "Pandas, NumPy, scikit-learn y matplotlib."},
    ]
    return base


def seed_conversation_via_posts(spec: Dict[str, Any]) -> Optional[int]:
    """Hace POST /chat por cada turno de usuario del seed y devuelve el
    conversation_id con la conversacion ya poblada en SQLite. Las metricas
    de estas llamadas se descartan: solo se usan para construir contexto."""

    history_key = spec["setup"]
    history = (
        seed_history_short()
        if history_key == "seed_history_short"
        else seed_history_long()
    )

    conv_id: Optional[int] = None
    base_run = spec["run_params"]

    for msg in history:
        if msg["role"] != "user":
            continue

        payload = {
            **base_run,
            "model": MODEL,
            "message": msg["content"],
            "conversation_id": conv_id,
        }
        data = post_chat(payload)
        if not data or "_error" in data:
            return None
        conv_id = data["conversation_id"]

    return conv_id


def execute_scenario(spec: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    needs_seed = "setup" in spec
    runs = RUNS_PER_SCENARIO

    for i in range(1, runs + 1):
        seed_conv_id: Optional[int] = None
        if needs_seed:
            seed_conv_id = seed_conversation_via_posts(spec)
            if seed_conv_id is None:
                rows.append({"i": i, "ok": False, "raw_error": "seed failed"})
                continue

        if needs_seed:
            payload = {
                **spec["run_params"],
                "message": spec["user_message"],
                "conversation_id": seed_conv_id,
            }
        else:
            payload = spec["run"](i)

        payload["model"] = MODEL

        t0 = time.perf_counter()
        data = post_chat(payload)
        t1 = time.perf_counter()

        row = {
            "i": i,
            "elapsed_s": round(t1 - t0, 3),
            "ok": "_error" not in (data or {}),
            "raw_error": (data or {}).get("_error"),
            "seeded_history": needs_seed,
            "seed_turns": {
                "seed_history_short": 2,
                "seed_history_long": 9,
            }.get(spec.get("setup", ""), 0),
        }

        if row["ok"]:
            metrics = data.get("metrics", {})
            # Este backend expone: prompt_eval_count, eval_count, total_tokens,
            # wall_time_s, total_duration_s, tokens_per_second.
            row.update({
                "prompt_tokens": int(metrics.get("prompt_eval_count", 0)),
                "completion_tokens": int(metrics.get("eval_count", 0)),
                "total_tokens": int(metrics.get("total_tokens", 0)),
                "wall_time_s": float(metrics.get("wall_time_s", 0.0)),
                "provider_duration_s": float(metrics.get("total_duration_s", 0.0)),
                "tokens_per_second": float(metrics.get("tokens_per_second", 0.0)),
                "reply_len": len(data.get("reply", "")),
            })

        rows.append(row)

    return {"spec": {k: v for k, v in spec.items() if k not in ("run",)}, "rows": rows}


METRIC_FIELDS = (
    "wall_time_s",
    "provider_duration_s",
    "prompt_tokens",
    "completion_tokens",
    "total_tokens",
    "tokens_per_second",
    "reply_len",
)


def aggregate(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    ok_rows = [r for r in rows if r.get("ok")]
    failed = [r for r in rows if not r.get("ok")]

    agg: Dict[str, Any] = {
        "n_total": len(rows),
        "n_ok": len(ok_rows),
        "n_failed": len(failed),
        "errors": sorted({r.get("raw_error") for r in failed if r.get("raw_error")}),
    }

    if not ok_rows:
        return agg

    for field in METRIC_FIELDS:
        values = [r[field] for r in ok_rows if field in r]
        if not values:
            continue
        agg[field] = {
            "mean": round(statistics.fmean(values), 4),
            "median": round(statistics.median(values), 4),
            "min": round(min(values), 4),
            "max": round(max(values), 4),
            "stdev": round(statistics.pstdev(values), 4) if len(values) > 1 else 0.0,
            "n": len(values),
        }

    return agg


def fmt_metric(agg: Dict[str, Any], field: str) -> str:
    m = agg.get(field)
    if not m:
        return "n/a"
    return (
        f"mean={m['mean']:.3f} | med={m['median']:.3f} | "
        f"min={m['min']:.3f} | max={m['max']:.3f} | std={m['stdev']:.3f}"
    )


def print_summary(results: List[Dict[str, Any]]) -> None:
    print(f"\nModelo: {MODEL}    Runs/escenario: {RUNS_PER_SCENARIO}\n")
    for r in results:
        spec = r["spec"]
        agg = aggregate(r["rows"])
        print("=" * 72)
        print(f"{spec['id']} - {spec['name']}")
        print(f"  {spec['description']}")
        print(f"  runs ok / total: {agg['n_ok']} / {agg['n_total']}")
        if agg.get("errors"):
            print(f"  errores: {agg['errors']}")
        for field in METRIC_FIELDS:
            print(f"  {field:<22} {fmt_metric(agg, field)}")
    print("=" * 72)


def generate_charts(summary: Dict[str, Any]) -> None:
    if not HAS_MPL:
        print("  [charts] matplotlib no disponible — omitiendo gráficas")
        return

    scenarios = summary["scenarios"]
    ids = [s["id"] for s in scenarios]
    names = [s["name"] for s in scenarios]
    labels = [f"{s['id']}\n{s['name'].split('(')[0].strip()[:20]}" for s in scenarios]

    def agg(sc, field):
        return sc["aggregate"].get(field, {})

    def mean(sc, field):
        m = agg(sc, field)
        return m.get("mean", 0) if m else 0

    def stdev(sc, field):
        m = agg(sc, field)
        return m.get("stdev", 0) if m else 0

    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
    })

    # ── Chart 1: Wall time ──
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(scenarios))
    means_wt = [mean(s, "wall_time_s") for s in scenarios]
    stds_wt = [stdev(s, "wall_time_s") for s in scenarios]
    bars = ax.bar(x, means_wt, yerr=stds_wt, capsize=5, color="steelblue", edgecolor="navy")
    ax.set_xticks(list(x))
    ax.set_xticklabels(ids, fontsize=10)
    ax.set_ylabel("Tiempo (s)")
    ax.set_title("Tiempo de Respuesta por Escenario (mean ± stdev)")
    ax.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, means_wt):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f"{val:.2f}s", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    p1 = CHART_DIR / "chart_wall_time.png"
    fig.savefig(p1, dpi=200)
    plt.close(fig)
    print(f"  [charts] {p1}")

    # ── Chart 2: Tokens/s ──
    fig, ax = plt.subplots(figsize=(10, 5))
    means_tps = [mean(s, "tokens_per_second") for s in scenarios]
    stds_tps = [stdev(s, "tokens_per_second") for s in scenarios]
    bars = ax.bar(x, means_tps, yerr=stds_tps, capsize=5, color="seagreen", edgecolor="darkgreen")
    ax.set_xticks(list(x))
    ax.set_xticklabels(ids, fontsize=10)
    ax.set_ylabel("Tokens/s")
    ax.set_title("Velocidad de Generación por Escenario (mean ± stdev)")
    ax.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, means_tps):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f"{val:.1f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    p2 = CHART_DIR / "chart_tokens_per_second.png"
    fig.savefig(p2, dpi=200)
    plt.close(fig)
    print(f"  [charts] {p2}")

    # ── Chart 3: Prompt vs Completion tokens ──
    fig, ax = plt.subplots(figsize=(10, 5))
    w = 0.35
    prompt_m = [mean(s, "prompt_tokens") for s in scenarios]
    complet_m = [mean(s, "completion_tokens") for s in scenarios]
    bars1 = ax.bar([i - w / 2 for i in x], prompt_m, w, label="Prompt (entrada)", color="coral", edgecolor="darkred")
    bars2 = ax.bar([i + w / 2 for i in x], complet_m, w, label="Completion (salida)", color="goldenrod", edgecolor="darkgoldenrod")
    ax.set_xticks(list(x))
    ax.set_xticklabels(ids, fontsize=10)
    ax.set_ylabel("Tokens")
    ax.set_title("Tokens de Entrada vs Salida por Escenario")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 5, f"{int(h)}", ha="center", va="bottom", fontsize=7)
    fig.tight_layout()
    p3 = CHART_DIR / "chart_prompt_vs_completion.png"
    fig.savefig(p3, dpi=200)
    plt.close(fig)
    print(f"  [charts] {p3}")

    # ── Chart 4: Context growth (S1, S2, S8) ──
    fig, ax = plt.subplots(figsize=(8, 5))
    ctx_ids = ["S1\n(sin historial)", "S2\n(2 turnos)", "S8\n(9 turnos)"]
    ctx_data = [mean(s, "prompt_tokens") for s in scenarios if s["id"] in ("S1", "S2", "S8")]
    ctx_x = list(range(len(ctx_data)))
    ax.plot(ctx_x, ctx_data, "o-", color="darkviolet", linewidth=2.5, markersize=10)
    ax.set_xticks(ctx_x)
    ax.set_xticklabels(ctx_ids, fontsize=10)
    ax.set_ylabel("Tokens de entrada (prompt)")
    ax.set_title("Crecimiento del Contexto Conversacional")
    ax.grid(axis="y", alpha=0.3)
    for i, val in enumerate(ctx_data):
        ax.annotate(f"{int(val)} tok\n(x{val / ctx_data[0]:.1f})", (i, val),
                    textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=9, color="darkviolet", fontweight="bold")
    fig.tight_layout()
    p4 = CHART_DIR / "chart_context_growth.png"
    fig.savefig(p4, dpi=200)
    plt.close(fig)
    print(f"  [charts] {p4}")

    # ── Chart 5: num_predict vs wall time ──
    fig, ax = plt.subplots(figsize=(8, 5))
    np_labels = {
        "S6": ("num_predict=60", 60),
        "S1": ("num_predict=160", 160),
        "S7": ("num_predict=300", 300),
        "S3": ("num_predict=400", 400),
    }
    np_scenarios = [s for s in scenarios if s["id"] in np_labels]
    np_names = [np_labels[s["id"]][0] for s in np_scenarios]
    np_vals = [np_labels[s["id"]][1] for s in np_scenarios]
    np_wt = [mean(s, "wall_time_s") for s in np_scenarios]
    np_std = [stdev(s, "wall_time_s") for s in np_scenarios]
    bars = ax.bar(range(len(np_scenarios)), np_wt, yerr=np_std, capsize=5,
                  color=["lightcoral", "steelblue", "mediumseagreen", "darkorange"],
                  edgecolor="black")
    ax.set_xticks(range(len(np_scenarios)))
    ax.set_xticklabels([f"{n}\n({v} tok)" for n, v in zip(np_names, np_vals)], fontsize=9)
    ax.set_ylabel("Tiempo (s)")
    ax.set_xlabel("Configuración de num_predict")
    ax.set_title("Impacto de num_predict en Tiempo de Respuesta")
    ax.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, np_wt):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f"{val:.2f}s", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    p5 = CHART_DIR / "chart_num_predict.png"
    fig.savefig(p5, dpi=200)
    plt.close(fig)
    print(f"  [charts] {p5}")

    print(f"  [charts] Todas las gráficas guardadas en {CHART_DIR}")


def main() -> int:
    scenarios = build_scenarios()
    print(f"Backend: {BACKEND_URL}")
    print(f"Escenarios: {len(scenarios)}    Runs/escenario: {RUNS_PER_SCENARIO}")

    results: List[Dict[str, Any]] = []
    total_runs = 0
    total_ok = 0
    t_start = time.perf_counter()

    for spec in scenarios:
        print(f"\n>>> Ejecutando {spec['id']} - {spec['name']}...", flush=True)
        result = execute_scenario(spec)
        agg = aggregate(result["rows"])
        results.append(result)
        total_runs += agg["n_total"]
        total_ok += agg["n_ok"]
        print(
            f"    {agg['n_ok']}/{agg['n_total']} ok | "
            f"wall mean={agg.get('wall_time_s', {}).get('mean', 'n/a')} | "
            f"tps mean={agg.get('tokens_per_second', {}).get('mean', 'n/a')}"
        )

    elapsed = time.perf_counter() - t_start

    summary = {
        "model": MODEL,
        "backend_url": BACKEND_URL,
        "runs_per_scenario": RUNS_PER_SCENARIO,
        "total_runs": total_runs,
        "total_ok": total_ok,
        "wall_time_total_s": round(elapsed, 2),
        "scenarios": [
            {
                "id": r["spec"]["id"],
                "name": r["spec"]["name"],
                "description": r["spec"]["description"],
                "aggregate": aggregate(r["rows"]),
            }
            for r in results
        ],
    }

    raw_path = OUT_DIR / f"metrics_raw_{RUN_TAG}.json"
    summary_path = OUT_DIR / f"metrics_summary_{RUN_TAG}.json"
    raw_path.write_text(
        json.dumps({"model": MODEL, "elapsed_s": round(elapsed, 2), "results": results}, indent=2, ensure_ascii=False)
    )
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

    print_summary(results)
    print(f"\nTotal runs: {total_runs} (ok {total_ok})")
    print(f"Tiempo total bateria: {elapsed:.1f} s")
    print(f"JSON raw:   {raw_path}")
    print(f"JSON summary: {summary_path}")

    generate_charts(summary)

    return 0 if total_ok == total_runs else 1


if __name__ == "__main__":
    sys.exit(main())
