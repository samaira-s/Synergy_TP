# Task 10 — Practical Regression Using ML Libraries

## Overview
Predicts Temperature from 5 sensor readings using scikit-learn regression
models (DummyRegressor baseline, LinearRegression, Ridge, DecisionTreeRegressor,
RandomForestRegressor).

## Folder Structure
- `data/` — Data.csv (source dataset)
- `notebook/` — training notebook with full pipeline, EDA, evaluation
- `model/` — final_regression_pipeline.joblib (saved RandomForest pipeline, max_depth=4)
- `output/` — metrics_comparison.csv, high_error_predictions.csv, plots, predictions_output.csv
- `inference/` — predict.py (standalone inference script), test_input.csv
- `report/` — Task10_Report.docx

## Setup
```bash
pip install pandas numpy scikit-learn matplotlib joblib
```

## Running the training notebook
Open `notebook/task_10.5.ipynb` and run all cells top to bottom.

## Running inference
From inside `inference/`:

Single hardcoded example:
```bash
python predict.py
```

Predict from a CSV of new records (no Temperature column):
```bash
python predict.py test_input.csv
```
Output is saved to `output/predictions_output.csv`.

## Final Model
RandomForestRegressor (n_estimators=200, max_depth=4, random_state=42),
selected after comparing against DummyRegressor baseline, LinearRegression,
Ridge, and DecisionTreeRegressor. See report for full justification.

## Key Finding
All sensor features show weak linear and monotonic correlation with Temperature.
No model substantially outperforms the mean-prediction baseline, indicating
limited predictive signal in the available features.