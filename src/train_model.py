"""Run reproducible ChemProp 1.6.1 multi-task cross-validation."""

from __future__ import annotations

import argparse
from pathlib import Path

import chemprop


TARGETS = ("S1_energy", "T1_energy", "ST_GAP(eV)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-workers", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    cli = parse_args()
    cli.save_dir.mkdir(parents=True, exist_ok=True)

    arguments = [
        "--data_path", str(cli.data),
        "--dataset_type", "regression",
        "--save_dir", str(cli.save_dir),
        "--epochs", str(cli.epochs),
        "--num_folds", str(cli.folds),
        "--ensemble_size", "1",
        "--num_workers", str(cli.num_workers),
        "--smiles_columns", "smiles",
        "--target_columns", *TARGETS,
        "--target_weights", "1", "1", "1",
        "--split_type", "random",
        "--split_sizes", "0.8", "0.1", "0.1",
        "--seed", str(cli.seed),
        "--pytorch_seed", str(cli.seed),
        "--hidden_size", "300",
        "--depth", "3",
        "--metric", "rmse",
    ]
    train_args = chemprop.args.TrainArgs().parse_args(arguments)
    mean_score, std_score = chemprop.train.cross_validate(
        args=train_args,
        train_func=chemprop.train.run_training,
    )
    print(f"overall_test_rmse={mean_score:.6f} +/- {std_score:.6f}")


if __name__ == "__main__":
    main()
