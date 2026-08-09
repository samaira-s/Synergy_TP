# Crop Recommendation — Classification Pipeline (Task 11)

## Overview
This project trains a multiclass classification model to recommend the most
suitable crop based on soil nutrients (N, P, K) and climate conditions
(temperature, humidity, pH, rainfall). Dataset: `Crop_recommendation.csv`
(2200 rows, 22 balanced crop classes).

## Folder Structure

```
Task_11/
│
├── data/
│   └── Crop_recommendation.csv         
│
├── inference/
│   ├── crop_recommendation_model.joblib 
│   ├── error_analysis.csv               
│   └── model_comparison_metrics.csv     
│
├── plots/
│   ├── confusion_matrix_rf.png         
│   └── model_comparison.png             
│
├── report/
│   └── Task11_Report.pdf                
│
├── predict.py                          
├── README.md                            
└── task_11.ipynb                        
```

## Setup

1. Install dependencies:
pip install pandas scikit-learn joblib matplotlib seaborn
2. Ensure these files are in the same folder:
   - `Crop_recommendation.csv`
   - `crop_recommendation_model.joblib` (trained model)
   - `predict.py` (inference script)

## Running the training pipeline

Open and run the notebook (`.ipynb`) top to bottom. It will:
- Load and explore the dataset
- Split data 70/15/15 (train/val/test, stratified)
- Train a majority-class baseline (DummyClassifier)
- Train and compare 4 models: Logistic Regression, KNN, Decision Tree, Random Forest
- Evaluate the best model (Random Forest) on the held-out test set
- Save the final trained pipeline as `crop_recommendation_model.joblib`

## Running predictions

From the terminal, inside the `Task_11/` root folder (not inside a subfolder):
python predict.py <N> <P> <K> <temperature> <humidity> <ph> <rainfall>
Example:python predict.py 90 42 43 20.8 82.0 6.5 202.9
Output:
Recommended crop: rice
Confidence: 97.50%
## Results Summary

| Model | Accuracy | F1 (macro) |
|---|---|---|
| Dummy Baseline | 4.5% | 0.004 |
| Logistic Regression | 96.7% | 0.966 |
| KNN | 98.5% | 0.985 |
| Decision Tree | 97.6% | 0.975 |
| **Random Forest (final)** | **99.1% (val) / 99.7% (test)** | **0.991 (val) / 0.997 (test)** |

## Files
- `crop_recommendation_model.joblib` — final trained pipeline
- `predict.py` — standalone inference script
- `confusion_matrix_rf.png` — confusion matrix on validation set
- `model_comparison.png` — bar chart comparing all models