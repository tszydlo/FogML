#!/usr/bin/env python3
"""OPS-SAT-AD anomaly detection over a per-channel telemetry CSV.

Python analogue of FogML-C's src/main.c (https://github.com/tszydlo/FogML-C):
reads a channel CSV produced by dataset/split_by_channel.py, and for each row
either updates the reservoir-sampled LOF model (fogml_learning, for
non-anomalous training rows) or scores the row against it
(fogml_processing, for non-training rows), printing per-row output and a
final accuracy summary — see examples/sat/README.md for the CSV shape.

Usage: python3 main.py <channel.csv>
"""

import argparse
import csv
import sys

from fogml_config import SatPipeline

# Feature columns of a dataset CSV row, in the order they appear after the
# 7 metadata columns (segment,anomaly,train,channel,sampling,duration,len).
FEATURE_NAMES = (
    "mean",
    "var",
    "std",
    "kurtosis",
    "skew",
    "n_peaks",
    "smooth10_n_peaks",
    "smooth20_n_peaks",
    "diff_peaks",
    "diff2_peaks",
    "diff_var",
    "diff2_var",
    "gaps_squared",
    "len_weighted",
    "var_div_duration",
    "var_div_len",
)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("channel_csv", help="Path to a per-channel CSV (see dataset/README.md)")
    return parser.parse_args()


def main():
    args = parse_args()

    pipeline = SatPipeline()

    total_lines = 0
    train_lines = 0
    matched_count = 0

    try:
        with open(args.channel_csv, newline="") as fp:
            reader = csv.DictReader(fp)

            for row in reader:
                anomaly = int(row["anomaly"])
                train = int(row["train"])
                features = [float(row[name]) for name in FEATURE_NAMES]

                print(
                    f"segment={row['segment']} anomaly={anomaly} train={train} "
                    f"channel={row['channel']} sampling={row['sampling']} "
                    f"duration={row['duration']} len={row['len']}"
                )

                # FogML Learning - only for training rows, and only normal (good) data for training
                if train and not anomaly:
                    pipeline.fogml_learning(features)

                # FogML Processing - only for rows not belonging to the training split
                if not train:
                    score = pipeline.fogml_processing(features)
                    print(f"score={score:.6f}")

                    detected_anomaly = 1 if score > pipeline.config.anomaly_threshold else 0
                    if detected_anomaly == anomaly:
                        matched_count += 1

                total_lines += 1
                if train:
                    train_lines += 1
    except FileNotFoundError:
        print(f"Error: could not open file '{args.channel_csv}'")
        return 1

    print(f"Train lines: {train_lines} / {total_lines}")
    print(f"Matched count: {matched_count}")

    if train_lines > 0:
        accuracy = matched_count / (total_lines - train_lines)
        print(f"Accuracy: {accuracy:.6f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
