import csv
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "graficas_resultados"
CSV_PATH = OUTPUT_DIR / "resultados.csv"
LABELS = ["on", "off", "none"]


def main():
    df = pd.read_csv(CSV_PATH)
    df["expected_action"] = df["expected_action"].fillna("none")
    df["predicted_action"] = df["predicted_action"].fillna("invalid")
    y_true = df["expected_action"].tolist()
    y_pred = df["predicted_action"].tolist()

    n = len(df)
    accuracy = accuracy_score(y_true, y_pred)
    precisions, recalls, f1s, supports = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, zero_division=0
    )
    macro_f1 = float(np.mean(f1s))

    json_valid_rate = float(df["json_valid"].mean())
    mqtt_publish_rate = float(df["mqtt_published"].mean())
    arch_success_rate = float(df["architecture_success"].mean())
    total_latency = df["total_latency_s"].astype(float)
    p50 = float(total_latency.quantile(0.50))
    p95 = float(total_latency.quantile(0.95))
    p99 = float(total_latency.quantile(0.99))
    mean_latency = float(total_latency.mean())
    in_tok = df["prompt_tokens"].fillna(0).astype(float)
    out_tok = df["response_tokens"].fillna(0).astype(float)
    avg_in = float(in_tok.mean())
    avg_out = float(out_tok.mean())
    total_in = float(in_tok.sum())
    total_out = float(out_tok.sum())

    COST_PER_1M_IN = 0.05
    COST_PER_1M_OUT = 0.08
    cost_in = (total_in / 1_000_000) * COST_PER_1M_IN
    cost_out = (total_out / 1_000_000) * COST_PER_1M_OUT
    cost = cost_in + cost_out

    cm = confusion_matrix(y_true, y_pred, labels=LABELS)

    print("=" * 60)
    print("MÉTRICAS DE CLASIFICACIÓN")
    print("=" * 60)
    print(f"Accuracy:                    {accuracy:.4f}")
    print(f"Macro F1:                    {macro_f1:.4f}")
    for label, p, r, f, s in zip(LABELS, precisions, recalls, f1s, supports):
        print(f"  Clase {label:5s}  P={p:.3f}  R={r:.3f}  F1={f:.3f}  support={s}")
    print()
    print("=" * 60)
    print("MÉTRICAS DE ARQUITECTURA")
    print("=" * 60)
    print(f"JSON validity rate:          {json_valid_rate:.4f}")
    print(f"MQTT publish rate:           {mqtt_publish_rate:.4f}")
    print(f"Architecture success rate:   {arch_success_rate:.4f}")
    print()
    print("=" * 60)
    print("MÉTRICAS DE OPERACIÓN")
    print("=" * 60)
    print(f"Latencia media total (s):    {mean_latency:.4f}")
    print(f"Latencia P50 (s):            {p50:.4f}")
    print(f"Latencia P95 (s):            {p95:.4f}")
    print(f"Latencia P99 (s):            {p99:.4f}")
    print(f"Tokens entrada promedio:     {avg_in:.1f}")
    print(f"Tokens salida promedio:      {avg_out:.1f}")
    print(f"Costo estimado (USD, {n} runs):")
    print(f"  Input  ({total_in:.0f} tok × $0.05/M):  ${cost_in:.6f}")
    print(f"  Output ({total_out:.0f} tok × $0.08/M): ${cost_out:.6f}")
    print(f"  Total:                                   ${cost:.6f}")

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(LABELS)))
    ax.set_yticks(range(len(LABELS)))
    ax.set_xticklabels(LABELS)
    ax.set_yticklabels(LABELS)
    ax.set_xlabel("Predicho")
    ax.set_ylabel("Esperado")
    ax.set_title(f"Matriz de confusión (n={n})")
    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            color = "white" if cm[i, j] > cm.max() / 2 else "black"
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", color=color)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(range(1, n + 1), total_latency.values, marker="o", markersize=3, linewidth=0.8)
    ax.axhline(p50, color="green", linestyle="--", label=f"P50={p50:.3f}s")
    ax.axhline(p95, color="orange", linestyle="--", label=f"P95={p95:.3f}s")
    ax.axhline(p99, color="red", linestyle="--", label=f"P99={p99:.3f}s")
    ax.set_xlabel("Número de prueba")
    ax.set_ylabel("Latencia total (s)")
    ax.set_title("Latencia por ejecución")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "latencias.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(out_tok.values, total_latency.values, alpha=0.6, s=20)
    ax.set_xlabel("Tokens de salida")
    ax.set_ylabel("Latencia total (s)")
    ax.set_title("Tokens vs Latencia")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "tokens_vs_latency.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    rates = {
        "JSON válido": json_valid_rate,
        "MQTT publicado": mqtt_publish_rate,
        "Architecture OK": arch_success_rate,
        "Accuracy": accuracy,
    }
    ax.bar(rates.keys(), rates.values(), color=["#4c72b0", "#dd8452", "#55a868", "#c44e52"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Tasa")
    ax.set_title("Tasas de éxito")
    for k, v in rates.items():
        ax.text(k, v + 0.02, f"{v:.2f}", ha="center")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "success_rates.png", dpi=120)
    plt.close(fig)

    print()
    print(f"Gráficas guardadas en {OUTPUT_DIR}/")
    for png in ["confusion_matrix.png", "latencias.png", "tokens_vs_latency.png", "success_rates.png"]:
        print(f"  - {png}")


if __name__ == "__main__":
    main()