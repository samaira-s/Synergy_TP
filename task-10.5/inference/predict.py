import sys
import joblib
import pandas as pd

def load_model(model_path="../model/final_regression_pipeline.joblib"):
    return joblib.load(model_path)

def predict_from_csv(model, input_csv):
    new_data = pd.read_csv(input_csv)
    predictions = model.predict(new_data)
    new_data["Predicted_Temperature"] = predictions
    return new_data

def predict_single(model, sensor_values: dict):
    df_row = pd.DataFrame([sensor_values])
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
            "Sensor1": 0.5,
            "Sensor2": 0.5,
            "Sensor3": 0.5,
            "Sensor4": 0.5,
            "Sensor5": 0.5,
        }
        pred = predict_single(model, example)
        print(f"Predicted Temperature: {pred:.2f}")