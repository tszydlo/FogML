# OPSSAT-AD dataset preparation

This folder prepares the [OPS-SAT-AD](https://github.com/kplabs-pl/OPS-SAT-AD) benchmark dataset
for the `examples/sat` anomaly detection example, by splitting it into one CSV file per telemetry
channel. Ported from [FogML-C](https://github.com/tszydlo/FogML-C)'s `dataset/` folder.

## Usage

1. Download `dataset.csv` from the Zenodo record (DOI
   [10.5281/zenodo.12588359](https://doi.org/10.5281/zenodo.12588359)) and place it in this
   folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python split_by_channel.py`

This produces one file per channel, e.g. `CADC0872.csv`, `CADC0873.csv`, ..., `CADC0894.csv`
(9 files total). Each file's first line is the same header/legend as `dataset.csv`, and each row
is one labeled telemetry segment for that channel, with columns:

```
segment,anomaly,train,channel,sampling,duration,len,mean,var,std,kurtosis,skew,n_peaks,
smooth10_n_peaks,smooth20_n_peaks,diff_peaks,diff2_peaks,diff_var,diff2_var,gaps_squared,
len_weighted,var_div_duration,var_div_len
```

- `anomaly`: 1 if the segment is labeled anomalous, 0 otherwise.
- `train`: 1 if the segment belongs to the training split, 0 otherwise.
- The remaining columns are statistical features extracted from the raw signal for that segment.

These per-channel CSVs are not committed to this repo (see the root `.gitignore`) — generate them
locally with the steps above before running `../main.py`.
