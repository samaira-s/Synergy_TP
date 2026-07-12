# Task 10 — Baseline Machine Learning from Scratch using AirQualityUCI

## Task Title and Description
A complete baseline ML workflow — implemented entirely from scratch, without scikit-learn or
any ready-made ML library — covering regression, classification, and clustering on the
AirQualityUCI dataset. Includes responsible train/validation/test splitting, baseline
predictors, manually implemented models and metrics, and written technical interpretation.

## Dataset Source
**AirQualityUCI**, from the UCI Machine Learning Repository:
https://archive.ics.uci.edu/dataset/360/air+quality

## Implemented Models
- **Linear Regression** (gradient descent, from scratch) — predicts `CO(GT)`.
- **Binary Logistic Regression** (gradient descent, from scratch) — predicts a derived
  `pollution_class` label (high vs. low pollution, split at the training median of `CO(GT)`).
- **KMeans clustering** (from scratch) — groups rows by `T` (temperature) and `RH` (relative
  humidity), with no label involved.
- **Baselines**: mean-prediction (regression) and majority-class (classification), used as the
  minimum bar every real model must beat.

## No Scikit-Learn / Ready-Made ML Library Used
Confirmed: this implementation uses only **pandas** (data loading/handling), **NumPy**
(numerical operations), and **matplotlib** (plots). No scikit-learn, XGBoost, LightGBM,
TensorFlow, PyTorch, Keras, statsmodels, or similar library was used anywhere. Every model,
baseline, and metric was implemented in-house in `src/`.

## How to Run
```bash
python task_10/src/main.py task_10/data/AirQualityUCI.csv task_10/output
```
This single command runs the full pipeline (regression, classification, clustering) and
regenerates every file in `task_10/output/` from scratch.

## Folder Structure
```
task_10/
├── README.md
├── theory/
│   └── Task_10_ML_Theory_Notes.pdf
├── data/
│   └── AirQualityUCI.csv
├── output/
│   ├── regression_metrics.json
│   ├── classification_metrics.json
│   ├── clustering_metrics.json
│   ├── regression_predictions.csv
│   ├── classification_predictions.csv
│   ├── clustering_assignments.csv
│   ├── regression_loss_curve.png
│   ├── classification_loss_curve.png
│   ├── actual_vs_predicted.png
│   ├── confusion_matrix.png
│   ├── clustering_plot.png
│   ├── model_comparison.md
│   └── error_analysis.md
└── src/
    ├── data_utils.py
    ├── metrics.py
    ├── baselines.py
    ├── linear_regression_gd.py
    ├── logistic_regression_gd.py
    ├── kmeans.py
    └── main.py
```

## Generated Outputs — What Each File Contains

| File | Contents |
|---|---|
| `regression_metrics.json` | Model & baseline MAE/RMSE/R², learned weights and bias |
| `classification_metrics.json` | Model & baseline accuracy/precision/recall/F1, confusion matrix counts, threshold used |
| `clustering_metrics.json` | k, iterations to converge, inertia, silhouette score, per-cluster size/centroid |
| `regression_predictions.csv` | Actual vs. predicted CO(GT) for every test-set row |
| `classification_predictions.csv` | Actual vs. predicted pollution_class for every test-set row |
| `clustering_assignments.csv` | T, RH, and assigned cluster for every training-set row |
| `regression_loss_curve.png` | MSE loss vs. gradient descent iteration (linear regression) |
| `classification_loss_curve.png` | Log loss vs. gradient descent iteration (logistic regression) |
| `actual_vs_predicted.png` | Scatter of actual vs. predicted CO(GT), with a perfect-prediction reference line |
| `confusion_matrix.png` | Visual 2×2 confusion matrix for the classifier |
| `clustering_plot.png` | 2D plot of T vs. RH, colored by cluster, with centroids marked |
| `model_comparison.md` | Target/feature justification, model-vs-baseline comparison, leakage risks, dataset readiness for stronger models |
| `error_analysis.md` | Largest regression errors, classification mistakes, class balance check, cluster pattern check, model limitations |

## Feature / Target Design Decisions
- **Regression** — target: `CO(GT)`. Features: `PT08.S1(CO)`, `PT08.S2(NMHC)`, `PT08.S3(NOx)`,
  `PT08.S4(NO2)`, `PT08.S5(O3)`, `T`, `RH`, `AH`. Excluded `NMHC(GT)` (≈90% missing in the raw
  data, marked -200 — a known limitation of this dataset). Excluded `NOx(GT)`/`NO2(GT)` (other
  reference-analyzer pollutant readings — including them risks the model leaning on another
  lab measurement rather than the actual low-cost sensors, undermining the sensor-calibration
  framing of this task).
- **Classification** — label derived from `CO(GT)` via a **training-set-only** median split
  (`pollution_class`: 1 = above median, 0 = at/below). Same feature set as regression, with
  `CO(GT)` itself excluded since the label is derived from it.
- **Clustering** — features: `T`, `RH` only, chosen for direct 2D interpretability. No label
  used at any point.
- **Split** — chronological 70/15/15 train/validation/test (not random), since this is hourly
  time-series data and a random split would leak near-identical adjacent hours across the split.
- **Scaling & threshold** — both fit only on training data, then applied unchanged to
  validation/test, to avoid preprocessing/target leakage.

## What Was Learned
- A trained model's raw score means little without a baseline comparison — e.g. the
  majority-class baseline here scores over 50% accuracy without learning anything.
- Preprocessing statistics (scaling mean/std, classification threshold) must be computed from
  training data only — computing them from the full dataset is a real, easy-to-make leakage
  mistake (caught and fixed during this task's own development).
- Time-series data needs a chronological split, not a random one, to get an honest estimate of
  real-world generalization.
- R², accuracy, and inertia are each incomplete alone — pairing metrics (MAE+R², precision+recall,
  inertia+silhouette) and checking plots gives a fuller, less misleading picture of model quality.