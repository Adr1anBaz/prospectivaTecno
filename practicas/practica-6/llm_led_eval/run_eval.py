import csv
import time
import random
from pathlib import Path

import requests
from openpyxl import Workbook

from dataset import DATASET

API_URL = "http://localhost:8001/led-agent"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "graficas_resultados"
OUTPUT_DIR.mkdir(exist_ok=True)
NUM_RUNS = 110


def main():
    csv_path = OUTPUT_DIR / "resultados.csv"
    xlsx_path = OUTPUT_DIR / "supervision.xlsx"

    rows = []
    rng = random.Random(42)

    print(f"Ejecutando {NUM_RUNS} pruebas cíclicas contra {API_URL} ...")
    for i in range(NUM_RUNS):
        prompt, expected = rng.choice(DATASET)
        try:
            r = requests.post(API_URL, json={"prompt": prompt}, timeout=60)
            r.raise_for_status()
            data = r.json()
        except Exception as exc:
            print(f"[{i + 1}/{NUM_RUNS}] ERROR con prompt={prompt!r}: {exc}")
            continue
        row = {
            "run": i + 1,
            "prompt": prompt,
            "expected_action": expected,
            "predicted_action": data.get("action"),
            "correct": (data.get("action") == expected),
            "json_valid": data.get("json_valid"),
            "parse_error": data.get("parse_error"),
            "mqtt_published": data.get("mqtt_published"),
            "architecture_success": data.get("architecture_success"),
            "confidence": data.get("confidence"),
            "reason": data.get("reason"),
            "total_latency_s": data.get("total_latency_s"),
            "ollama_latency_s": data.get("ollama_latency_s"),
            "prompt_tokens": data.get("prompt_tokens"),
            "response_tokens": data.get("response_tokens"),
            "raw_response": (data.get("raw_response") or "")[:200],
        }
        rows.append(row)
        if (i + 1) % 10 == 0:
            acc_so_far = sum(r["correct"] for r in rows) / len(rows)
            print(f"[{i + 1}/{NUM_RUNS}] accuracy parcial={acc_so_far:.3f}")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV escrito en {csv_path} ({len(rows)} filas)")

    wb = Workbook()
    ws = wb.active
    ws.title = "supervision"
    headers = list(rows[0].keys())
    ws.append(headers)
    for row in rows:
        ws.append([row[h] for h in headers])
    for cell in ws[1]:
        cell.font = cell.font.copy(bold=True)
    wb.save(xlsx_path)
    print(f"Excel de supervisión escrito en {xlsx_path}")

    print("\nResumen:")
    print(f"  Pruebas:        {len(rows)}")
    print(f"  Accuracy:       {sum(r['correct'] for r in rows) / len(rows):.4f}")
    print(f"  JSON válido:    {sum(r['json_valid'] for r in rows) / len(rows):.4f}")
    print(f"  MQTT publicado: {sum(r['mqtt_published'] for r in rows) / len(rows):.4f}")


if __name__ == "__main__":
    main()