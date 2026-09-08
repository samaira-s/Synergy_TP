# Task 13 — Neural Networks: From Fundamentals to PyTorch

## Overview
Builds a small MLP twice — once entirely from scratch in NumPy (manual
forward pass, backprop, gradient descent), once properly in PyTorch — and
compares both against a classical Logistic Regression baseline on the same
data and preprocessing, to see whether the added complexity of a neural
network actually helps.

## Dataset
Pima Indians Diabetes Database (UCI / National Institute of Diabetes and
Digestive and Kidney Diseases). Binary classification: predict diabetes
onset (Outcome) from 8 clinical features (Pregnancies, Glucose,
BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age).
768 rows. Zero values in Glucose/BloodPressure/SkinThickness/Insulin/BMI
are treated as missing (physiologically impossible) and imputed with the
training-set median.

## Folder Structure
- `data/` — diabetes.csv
- `notebook/` — baseline_numpy.ipynb (preprocessing, Logistic Regression
  baseline, NumPy MLP from scratch), pytorch_mlp.ipynb (PyTorch MLP,
  dropout regularization experiment, final model comparison)
- `model/` — scaler.pkl, train_medians.pkl, numpy_mlp_weights.npz,
  diabetes_mlp.pth (final PyTorch checkpoint)
- `output/` — loss curve plots, dropout comparison plot, model comparison
  table, saved results JSON
- `inference/` — predict.py (standalone PyTorch inference script), test_input.csv
- `report/` — Task13_Report.docx (pending)

## Setup
```bash
pip install pandas numpy scikit-learn matplotlib joblib torch
```

## Running the notebooks
Run in order — `pytorch_mlp.ipynb` loads results saved by `baseline_numpy.ipynb`
from `output/baseline_numpy_results.json`, since the two run as separate
kernels and can't share variables directly:
1. `notebook/baseline_numpy.ipynb` — run top to bottom first
2. `notebook/pytorch_mlp.ipynb` — run top to bottom second

## Running inference
```bash
cd inference
python predict.py                      # single hardcoded example
python predict.py test_input.csv       # batch prediction from a CSV
```

## Models Compared
- Logistic Regression (classical baseline, scikit-learn)
- NumPy MLP (manual forward/backward pass, 8→8→1, ReLU + sigmoid)
- PyTorch MLP, no regularization (8→8→1, ReLU)
- PyTorch MLP, Dropout(0.3) — regularization experiment, compared
  before/after against the no-dropout version

See `output/model_comparison.csv` for full Accuracy/Precision/Recall/F1/
ROC-AUC/training-time numbers across all four models.

## Key Findings
- Logistic Regression was re-evaluated on scaled features (not raw) to
  keep the comparison against both MLPs fair.
- The NumPy MLP and PyTorch (no-reg) MLP perform comparably to each other,
  confirming the from-scratch implementation is mathematically correct.
- Dropout's effect on this small dataset/model was modest; the final
  checkpoint is automatically selected based on whichever variant (with or
  without dropout) achieved better validation F1.

## Status
Code, training, comparison, checkpointing, and inference script are complete
and verified working end-to-end. Full 10-section report is still pending.