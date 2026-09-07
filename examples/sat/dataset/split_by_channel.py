#!/usr/bin/env python3
"""Split the OPSSAT-AD dataset.csv into one CSV file per telemetry channel and sampling rate.

Ported near-verbatim from FogML-C's dataset/split_by_channel.py
(https://github.com/tszydlo/FogML-C).
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default=str(SCRIPT_DIR / "dataset.csv"),
        help="Path to the OPSSAT-AD dataset.csv file (default: dataset.csv next to this script)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(SCRIPT_DIR),
        help="Directory to write per-channel CSV files into (default: this script's directory)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        sys.exit(
            f"Input file not found: {input_path}\n"
            "Download dataset.csv from the OPSSAT-AD Zenodo record "
            "(DOI 10.5281/zenodo.12588359) and place it here, or pass --input."
        )

    df = pd.read_csv(input_path)
    for column in ("channel", "sampling"):
        if column not in df.columns:
            sys.exit(f"Expected a '{column}' column in {input_path}, found: {list(df.columns)}")

    output_dir.mkdir(parents=True, exist_ok=True)

    for channel in sorted(df["channel"].unique()):
        channel_df = df[df["channel"] == channel]
        for sampling in sorted(channel_df["sampling"].unique()):
            subset = channel_df[channel_df["sampling"] == sampling].sort_values("segment")
            out_path = output_dir / f"{channel}-{sampling}.csv"
            subset.to_csv(out_path, index=False)
            print(f"{out_path.name}: {len(subset)} rows")


if __name__ == "__main__":
    main()
