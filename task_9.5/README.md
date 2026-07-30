# Synergy – ML Domain Task 9.5

## Machine Learning: Regression and Classification

This repository contains the work completed for **Synergy Software/ML Domain – Task 9.5**.

The task includes two machine learning experiments implemented **from scratch without using scikit-learn or any ready-made ML model**.

### 1. Linear Regression

* Dataset: `oil_sales_assignment_dataset.csv`
* Target: `volume_sales`
* Model: Linear Regression
* Training method: Gradient Descent
* Features are standardized before training.
* Evaluation metrics used:

  * MAE
  * MSE
  * RMSE
  * R²
* A mean-target baseline is also used for comparison.

Notebook:

`task_9.5_linear_regression.ipynb`

### 2. Logistic Regression

* Dataset: `heart_disease_risk_2026.csv`
* Target: `has_heart_disease`
* Model: Logistic Regression
* Training method: Gradient Descent
* Sigmoid function and Binary Cross-Entropy are implemented manually.
* Evaluation metrics used:

  * Accuracy
  * Precision
  * Recall
  * F1-score
* Confusion matrix, threshold analysis and error analysis are also included.
* A majority-class baseline is used for comparison.

Notebook:

`task_9.5_logistic_regression.ipynb`

## Requirements

The notebooks use:

* Python 3
* NumPy
* Pandas
* Matplotlib
* Jupyter Notebook

No scikit-learn models are used.

## How to Run

1. Clone or download this repository.
2. Make sure the required CSV datasets are in the correct folder.
3. Open the required `.ipynb` file using Jupyter Notebook or JupyterLab.
4. Run the cells from top to bottom.
5. The notebooks will generate the model results, metrics and plots.

## Files

```
Task-9.5/
│
├── README.md
|__ data/
|   ├── oil_sales_assignment_dataset.csv
|   └── heart_disease_risk_2026.csv
|
├── regression/
│   └── task_9.5_linear_regression.ipynb
|
├── classification/
│   └── task_9.5_logistic_regression.ipynb
│   
│
└── report/
    └── task_9.5_Report.docx
```

## Summary

This task covers the basic theory and implementation of:

* Linear Regression
* Logistic Regression
* Gradient Descent
* Feature Scaling
* Model Evaluation
* Baseline Comparison
* Error Analysis
* Training, Validation and Test Splits
