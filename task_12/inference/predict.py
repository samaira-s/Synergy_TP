import sys
import joblib
import pandas as pd

FEATURES = ["Temperature", "Humidity", "Light", "CO2", "HumidityRatio"]

def load_model(model_path="../model/final_occupancy_model.joblib"):
    return joblib.load(model_path)

def predict_from_csv(model, input_csv):
    new_data = pd.read_csv(input_csv)
    predictions = model.predict(new_data[FEATURES])
    new_data["Predicted_Occupancy"] = predictions
    return new_data

def predict_single(model, sensor_values: dict):
    df_row = pd.DataFrame([sensor_values])[FEATURES]
    return model.predict(df_row)[0]

if __name__ == "__main__":
    model = load_model()

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        result = predict_from_csv(model, input_path)
        print(result)
        result.to_csv("../output/predictions_output.csv", index=False)
    else:
        example = {
            "Temperature": 21.0,
            "Humidity": 25.0,
            "Light": 450.0,
            "CO2": 700.0,
            "HumidityRatio": 0.004,
        }
        pred = predict_single(model, example)
        print(f"Predicted Occupancy: {pred} ({'Occupied' if pred == 1 else 'Empty'})")