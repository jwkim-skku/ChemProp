"""Validate molecular-property CSV files and derive the ST Gap target."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, Optional, Set, Tuple

import pandas as pd


REQUIRED_COLUMNS = ("uid", "smiles", "S1_energy", "T1_energy")
TARGET_COLUMN = "ST_GAP(eV)"


def load_invalid_uids(path: Optional[Path]) -> Set[str]:
    if path is None:
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def prepare_dataframe(
    frames: Iterable[pd.DataFrame],
    *,
    invalid_uids: Optional[Set[str]] = None,
    sample_size: Optional[int] = None,
    seed: int = 42,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Combine, validate, clean, and optionally sample input dataframes."""
    combined = pd.concat(list(frames), ignore_index=True)
    missing = sorted(set(REQUIRED_COLUMNS) - set(combined.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    summary = {"input_rows": int(len(combined))}
    cleaned = combined.loc[:, REQUIRED_COLUMNS].copy()
    cleaned["uid"] = cleaned["uid"].astype(str).str.strip()
    cleaned["smiles"] = cleaned["smiles"].astype(str).str.strip()
    cleaned["S1_energy"] = pd.to_numeric(cleaned["S1_energy"], errors="coerce")
    cleaned["T1_energy"] = pd.to_numeric(cleaned["T1_energy"], errors="coerce")

    before = len(cleaned)
    cleaned = cleaned.dropna(subset=list(REQUIRED_COLUMNS))
    cleaned = cleaned[(cleaned["uid"] != "") & (cleaned["smiles"] != "")]
    summary["removed_missing_or_invalid"] = int(before - len(cleaned))

    blocked = invalid_uids or set()
    before = len(cleaned)
    cleaned = cleaned[~cleaned["uid"].isin(blocked)]
    summary["removed_known_invalid_uids"] = int(before - len(cleaned))

    before = len(cleaned)
    cleaned = cleaned.drop_duplicates(subset=["smiles"], keep="first")
    summary["removed_duplicate_smiles"] = int(before - len(cleaned))

    cleaned[TARGET_COLUMN] = cleaned["S1_energy"] - cleaned["T1_energy"]

    if sample_size is not None:
        if sample_size <= 0:
            raise ValueError("sample_size must be positive")
        if sample_size > len(cleaned):
            raise ValueError(
                f"sample_size={sample_size} exceeds cleaned rows={len(cleaned)}"
            )
        cleaned = cleaned.sample(n=sample_size, random_state=seed)

    cleaned = cleaned.sort_values("uid").reset_index(drop=True)
    summary["output_rows"] = int(len(cleaned))
    return cleaned, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--invalid-uids", type=Path)
    parser.add_argument("--sample-size", type=int)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frames = [pd.read_csv(path) for path in args.inputs]
    cleaned, summary = prepare_dataframe(
        frames,
        invalid_uids=load_invalid_uids(args.invalid_uids),
        sample_size=args.sample_size,
        seed=args.seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(args.output, index=False)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
