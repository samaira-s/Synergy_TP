# Task 9 — Calibration Statistics, Correlation Analysis, and Feature Engineering

## 1. Task Title
Calibration Statistics, Correlation Analysis, and Feature Engineering

## 2. Objective
Convert raw, repeated domain measurements (Biochemistry, Electronics, Mechanical)
into statistically vetted, ML-ready data. This means: computing replicate-level
reliability statistics, checking whether measured signal changes predictably with
a controlled input (calibration + correlation), engineering domain-valid derived
features, and flagging which rows are actually trustworthy enough for machine
learning — not calculating any of it blindly.

## 3. How to Run
```bash
python task_9/src/main.py task_9/data/calibration_measurements.csv task_9/output
```
This single command regenerates every file in `task_9/output/` from scratch.

## 4. Folder Structure
```
task_9/
├── README.md
├── data/
│   └── calibration_measurements.csv
├── output/
│   ├── replicate_summary.csv
│   ├── calibration_summary.csv
│   ├── correlation_summary.csv
│   ├── engineered_features.csv
│   ├── ml_ready_dataset.csv
│   ├── replicate_analysis.md
│   ├── correlation_limitations.md
│   ├── feature_dictionary.md
│   ├── feature_summary.md
│   ├── calibration_curve_biochem.png
│   ├── calibration_curve_electronics.png
│   ├── calibration_curve_mechanical.png
│   └── correlation_signal_input.png
└── src/
    ├── replicate_statistics.py
    ├── correlation_analysis.py
    ├── feature_engineering.py
    └── main.py
```

## 5. Part-by-Part Summary

**Part 1 — Replicate Statistics** (`replicate_statistics.py`): Groups the dataset
by domain/condition/input, computes mean, median, sample variance, sample std,
standard error, 95% confidence interval (t-distribution, n-1 degrees of freedom),
coefficient of variation, and a stability flag (stable / moderate / unstable /
unreliable) per group.

**Part 2 — Calibration & Correlation** (`correlation_analysis.py`): For each
required relationship (Biochem signal-vs-concentration, Electronics
signal-vs-load, Electronics signal-vs-temperature, Mechanical signal-vs-load,
Mechanical stress-vs-load), computes Pearson and Spearman correlation, fits a
simple linear calibration line, and computes R², MAE, RMSE. Produces calibration
plots (mean signal ± 95% CI error bars) per domain, plus one raw scatter plot.

**Part 3 — Feature Engineering** (`feature_engineering.py`): Adds
`rolling_average_signal`, `normalized_signal`, `power_w` (Electronics only),
`error_percent`, `stress_ratio` (Mechanical only), `stability_flag`, and
`ml_ready`. Domain-invalid features are left blank (NaN), never forced to zero.

**Orchestration** (`main.py`): Runs all three parts, writes every CSV/plot, and
generates the four markdown interpretation files — computed dynamically from the
actual run's results (e.g. "most noisy group" is computed via code, not
hand-written), so re-running the pipeline on different data keeps the
interpretation accurate.

## 6. Key Results (from the sample dataset)
- **Most stable replicate group**: Electronics / low_load (CV ≈ 0.005)
- **Most noisy replicate group**: Mechanical / high_load (CV ≈ 0.10), driven by
  one reading (record M009) that deviates from its two replicate peers —
  flagged in `replicate_analysis.md` for investigation before trusting that
  group's mean.
- **Strongest signal-input relationship**: Biochem signal vs concentration
  (Pearson r ≈ 0.999, R² ≈ 0.999)
- **Weakest of the tested relationships**: Mechanical signal vs load
  (Pearson r ≈ 0.984, R² ≈ 0.968) — still strong, but noisier than the others,
  consistent with the Mechanical high_load group's instability.
- All rows in the sample dataset passed the `ml_ready` gate (complete required
  fields, and no replicate group was flagged fully "unstable").

## 7. What Was Learned
- Mean alone can't tell you whether a group of readings is trustworthy — you
  need the spread (std, SE, CI, CV) to know that.
- Standard error (not std) is what should shrink as replicate count grows —
  more repeats give a more precise *mean*, without necessarily making
  individual readings themselves any less noisy.
- Coefficient of variation lets you compare "noisiness" fairly across groups
  with very different scales (e.g. a 0.1mM reading vs. a 150N reading), where
  raw standard deviation numbers aren't directly comparable.
- A high Pearson correlation on a small sample (n=9 here) is suggestive, not
  proof — and Pearson specifically can miss real but non-linear relationships
  that Spearman (or a plot) would catch.
- Engineered features must be left blank, not zero, when they don't apply to a
  domain — forcing a 0 for `power_w` on a Biochem row would look like a real
  measurement of zero power, silently introducing false information.
- "ML-ready" isn't just "no missing values" — it also requires the row's
  replicate group to be statistically stable enough to trust.
