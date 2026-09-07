#!/usr/bin/env bash
#
# Runs every per-channel dataset CSV in dataset/ through main.py, one file at
# a time. Python analogue of FogML-C's run_all_channels.sh.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATASET_DIR="$SCRIPT_DIR/dataset"

shopt -s nullglob
csv_files=("$DATASET_DIR"/CADC*.csv)
shopt -u nullglob

if [ ${#csv_files[@]} -eq 0 ]; then
    echo "Error: no per-channel CSV files found in $DATASET_DIR" >&2
    echo "Run dataset/split_by_channel.py first (see dataset/README.md)." >&2
    exit 1
fi

for csv in "${csv_files[@]}"; do
    echo "=== $(basename "$csv") ==="
    python3 "$SCRIPT_DIR/main.py" "$csv"
    echo
done
