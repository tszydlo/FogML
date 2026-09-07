# sat — OPS-SAT-AD anomaly detection (Python port)

A Python port of [FogML-C](https://github.com/tszydlo/FogML-C): online, semi-supervised anomaly
detection on satellite telemetry (the [OPS-SAT-AD](https://github.com/kplabs-pl/OPS-SAT-AD)
benchmark), using `fogml_runtime`'s reservoir-sampling + LOF pipeline in place of the compiled C
FogML SDK. Same algorithm, same CSV-driven CLI shape, same output format — no C toolchain,
Makefile, or vendored SDK submodule required.

More details on the algorithms used are described in the paper
[arXiv:2206.14265](https://arxiv.org/abs/2206.14265).

## How this maps to FogML-C

| FogML-C (C)                          | This port (Python)          |
|---------------------------------------|------------------------------|
| `lib/fogml_sdk` (vendored C SDK)       | `fogml_runtime` (`src/fogml_runtime`) |
| `src/fogml_config.h` (pipeline config) | `fogml_config.py`             |
| `src/main.c` (CLI driver)              | `main.py`                     |
| `dataset/` (dataset prep)              | `dataset/` (ported near-verbatim) |
| `run_all_channels.sh`                  | `run_all_channels.sh`         |

`fogml_config.py` mirrors `fogml_config.h`: it defines `SatPipelineConfig` (reservoir size, LOF
`k`, vector size, anomaly-score threshold — the same knobs as the C globals) and `SatPipeline`,
whose `fogml_learning(vector)` / `fogml_processing(vector) -> score` methods are the same two
entry points the C file exposes as free functions.

## Getting the dataset

The OPS-SAT-AD dataset isn't vendored here (Zenodo-hosted, not bundled with this repo). See
[`dataset/README.md`](dataset/README.md): download `dataset.csv` from Zenodo (DOI
[10.5281/zenodo.12588359](https://doi.org/10.5281/zenodo.12588359)), `pip install -r
dataset/requirements.txt`, then run `python dataset/split_by_channel.py` to produce one CSV per
channel (e.g. `dataset/CADC0872-1.csv`).

## Usage

```bash
python3 main.py dataset/<channel>.csv
```

e.g. `python3 main.py dataset/CADC0886-5.csv`. Each per-channel CSV's first line is a
legend/header (skipped automatically); every row after that is one labeled segment. For each row
the program prints its metadata (`segment`, `anomaly`, `train`, `channel`, `sampling`,
`duration`, `len`), then:

* if the row belongs to the training split and is labeled non-anomalous (`train==1 &&
  anomaly==0`), its feature vector updates the reservoir-sampled LOF model
  (`pipeline.fogml_learning`);
* otherwise (`train==0`), the feature vector is scored against that model
  (`pipeline.fogml_processing`), the LOF `score` is printed, and the row is classified anomalous
  when `score > pipeline.config.anomaly_threshold` (default `1.5`, set in `fogml_config.py`) —
  that classification is then checked against the row's ground-truth `anomaly` label.

After all rows are processed, it prints `Train lines: X / Y`, `Matched count: Z`, and
`Accuracy: ...` — the fraction of non-training rows whose classification matched the
ground-truth label.

## Running all channels

```bash
./run_all_channels.sh
```

Runs every `dataset/CADC*.csv` file (the per-channel splits) through `main.py` in turn, printing
each channel's results and accuracy.

## Dependencies

Only what `fogml_runtime` already needs (`numpy`, `scikit-learn`) plus the Python standard
library — no extra install for `main.py` itself. `dataset/split_by_channel.py` additionally needs
`pandas` (see `dataset/requirements.txt`).

## Bibliography

Please mention us and cite our papers if you use this work and find it useful.

```
@misc{OnlineAnomalySzydlo2022,
  doi = {10.48550/ARXIV.2206.14265},
  url = {https://arxiv.org/abs/2206.14265},
  author = {Szydlo, Tomasz},
  keywords = {Machine Learning (cs.LG), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {Online Anomaly Detection Based On Reservoir Sampling and LOF for IoT devices},
  publisher = {arXiv},
  year = {2022},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```
