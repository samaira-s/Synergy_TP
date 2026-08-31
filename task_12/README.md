# Task 12 — Generalization, Robustness, and Anomaly Detection

## Overview
Investigates whether a RandomForestClassifier's reported performance on the
UCI Occupancy Detection dataset is trustworthy under realistic evaluation
conditions, or inflated by convenient (random) splitting. Covers split-strategy
comparison, run-to-run stability, unsupervised structure discovery, and a
robustness stress test against feature drift.

## Dataset
UCI Occupancy Detection Dataset (Candanedo & Feldheim, 2016).
5 features: Temperature, Humidity, Light, CO2, HumidityRatio.
Target: Occupancy (binary). Three files with real chronological/condition
structure:
- `datatraining.txt` — Feb 4–10, 2015 (train)
- `datatest.txt` — Feb 2–4, 2015, door-open condition (condition-shift test)
- `datatest2.txt` — Feb 11–18, 2015 (future / chronological test)

## Folder Structure
- `data/` — raw dataset files
- `notebook/` — full experiment notebook (splits, stability, clustering,
  anomaly detection, robustness test)
- `output/` — result tables (split comparison, stability repeats,
  contamination sensitivity, robustness test, feature importances,
  cluster/anomaly crosstabs)
- `report/` — Task12_Report.docx

## Setup
```bash
pip install pandas numpy scikit-learn matplotlib joblib
```

## Key Findings
1. **Naive random split overstates performance.** Random split F1 (0.980)
   vs. realistic chronological split F1 (0.938) — a ~4-point gap driven by
   near-duplicate timestamps leaking across train/test in the random split.
2. **Condition shift (door-open) hurts more than time alone.** F1 drops
   further to 0.929 when evaluated on a genuinely different environmental
   condition, not just a later date.
3. **Realistic splits are less stable, not just lower-scoring.** Across 5
   seeds, the realistic split's F1 standard deviation (0.0098) is ~3x the
   random split's (0.0032).
4. **Unsupervised structure partially aligns with occupancy** but is not a
   clean substitute for it (K-Means); anomalous readings (IsolationForest)
   are consistently more likely to be occupied rows than baseline, across
   multiple contamination thresholds.
5. **CO2 drifted ~24% between training and test periods** and was the
   model's 2nd most important feature — neutralizing it at test time
   *improved* performance, showing a heavily-used feature had become a
   liability due to drift.

## Final Model
RandomForestClassifier(n_estimators=200, random_state=42), trained on
`datatraining.txt`, evaluated under multiple realistic conditions rather
than a single train/test split. See report for full methodology and
discussion of which performance claims are defensible.