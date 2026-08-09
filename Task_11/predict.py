import sys
import joblib
import pandas as pd

def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    model = joblib.load('crop_recommendation_model.joblib')
    
    input_df = pd.DataFrame([{
        'N': N, 'P': P, 'K': K,
        'temperature': temperature, 'humidity': humidity,
        'ph': ph, 'rainfall': rainfall
    }])
    
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)
    
    return prediction, confidence

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python predict.py <N> <P> <K> <temperature> <humidity> <ph> <rainfall>")
        sys.exit(1)
    
    N, P, K, temperature, humidity, ph, rainfall = map(float, sys.argv[1:8])
    
    crop, confidence = predict_crop(N, P, K, temperature, humidity, ph, rainfall)
    print(f"Recommended crop: {crop}")
    print(f"Confidence: {confidence:.2%}")