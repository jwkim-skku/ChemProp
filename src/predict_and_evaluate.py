"""Predict molecular energies, create parity plots, and export error cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import chemprop
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


TARGETS = ("S1_energy", "T1_energy", "ST_GAP(eV)")


def plot_parity(y_true: pd.Series, y_pred: pd.Series, title: str, output: Path) -> None:
    low = min(float(y_true.min()), float(y_pred.min()))
    high = max(float(y_true.max()), float(y_pred.max()))
    pad = max((high - low) * 0.08, 0.05)
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    ax.scatter(y_true, y_pred, s=24, alpha=0.72, edgecolors="none")
    ax.plot([low - pad, high + pad], [low - pad, high + pad], "--", color="black")
    ax.set(xlabel="True (eV)", ylabel="Predicted (eV)", title=title)
    ax.set_xlim(low - pad, high + pad)
    ax.set_ylim(low - pad, high + pad)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test-data", type=Path, required=True)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--error-threshold", type=float, default=0.3)
    parser.add_argument("--num-workers", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prediction_csv = args.output_dir / "predictions.csv"

    predict_args = chemprop.args.PredictArgs().parse_args([
        "--test_path", str(args.test_data),
        "--preds_path", str(prediction_csv),
        "--checkpoint_dir", str(args.checkpoint_dir),
        "--smiles_columns", "smiles",
        "--num_workers", str(args.num_workers),
    ])
    predictions = np.asarray(chemprop.train.make_predictions(args=predict_args), dtype=float)
    if predictions.ndim != 2 or predictions.shape[1] != len(TARGETS):
        raise ValueError(f"Expected predictions with 3 targets, got {predictions.shape}")

    actual = pd.read_csv(args.test_data).copy()
    if "ST_GAP(eV)" not in actual:
        actual["ST_GAP(eV)"] = actual["S1_energy"] - actual["T1_energy"]

    pred_columns = [f"pred_{name}" for name in TARGETS]
    pred_df = pd.DataFrame(predictions, columns=pred_columns)
    combined = pd.concat([actual.reset_index(drop=True), pred_df], axis=1)

    metrics: Dict[str, Dict[str, float]] = {}
    for target, pred_col in zip(TARGETS, pred_columns):
        mae = mean_absolute_error(combined[target], combined[pred_col])
        rmse = mean_squared_error(combined[target], combined[pred_col], squared=False)
        metrics[target] = {"mae": float(mae), "rmse": float(rmse)}
        plot_parity(
            combined[target],
            combined[pred_col],
            f"{target}: true vs predicted",
            args.output_dir / f"parity_{target.replace('/', '_')}.png",
        )

    combined["abs_error_ST_GAP(eV)"] = (
        combined["ST_GAP(eV)"] - combined["pred_ST_GAP(eV)"]
    ).abs()
    combined.to_csv(args.output_dir / "predictions_with_errors.csv", index=False)
    error_cases = combined[
        combined["abs_error_ST_GAP(eV)"] > args.error_threshold
    ].sort_values("abs_error_ST_GAP(eV)", ascending=False)
    error_cases.to_csv(args.output_dir / "large_error_cases.csv", index=False)
    (args.output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    print(f"large_error_cases={len(error_cases)}")


if __name__ == "__main__":
    main()
