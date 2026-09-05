import os
import joblib
import numpy as np
import torch
import torch.nn as nn
import pandas as pd

# Paths

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "diabetes_mlp.pth")
SCALER_PATH = os.path.join(BASE_DIR, "..", "model", "scaler.pkl")
MEDIANS_PATH = os.path.join(BASE_DIR, "..", "model", "train_medians.pkl")



# Model definition
class DiabetesMLP(nn.Module):
    def __init__(self):
        super(DiabetesMLP, self).__init__()

        self.network = nn.Sequential(
            nn.Linear(8, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )

    def forward(self, x):
        return self.network(x)


# Load model and preprocessing

device = torch.device("cpu")

model = DiabetesMLP().to(device)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

model.eval()

scaler = joblib.load(SCALER_PATH)
train_medians = joblib.load(MEDIANS_PATH)



# Input data
# Feature order:
# Pregnancies, Glucose, BloodPressure,
# SkinThickness, Insulin, BMI,
# DiabetesPedigreeFunction, Age

patient = np.array([
    [2, 120, 70, 25, 80, 30.5, 0.5, 35]
], dtype=float)


# Apply same preprocessing

zero_columns = [1, 2, 3, 4, 5]

for col in zero_columns:
    if patient[0, col] == 0:
        feature_name = [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age"
        ][col]

        patient[0, col] = train_medians[feature_name]


feature_names = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

patient_df = pd.DataFrame(patient, columns=feature_names)

patient_scaled = scaler.transform(patient_df)



# Convert to tensor

X_tensor = torch.tensor(
    patient_scaled,
    dtype=torch.float32
).to(device)


# Prediction

with torch.no_grad():

    logits = model(X_tensor)

    probability = torch.sigmoid(logits).item()

    prediction = 1 if probability >= 0.5 else 0


# Display result

print("Diabetes Probability:", round(probability, 4))

if prediction == 1:
    print("Prediction: Diabetes")
else:
    print("Prediction: No Diabetes")