import numpy as np
import pickle
import requests

LOOKBACK = 24
MODEL_PATH = "model/lstm_hourly_pm25_model_70%.h5"
FEATURE_SCALER_PATH = "model/feature_scaler.pkl"
TARGET_SCALER_PATH = "model/target_scaler.pkl"

# load model
try:
    import tensorflow as tf
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    MODEL_AVAILABLE = True
except Exception as e:
    print(f"[predictor] TensorFlow unavailable: {e}")
    MODEL_AVAILABLE = False

with open (FEATURE_SCALER_PATH, "rb") as f:
    feature_scaler = pickle.load(f)

with open (TARGET_SCALER_PATH, "rb") as f:
    target_scaler = pickle.load(f)


def fetch_last_24h(lat, lon):
    aq_url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=pm10&past_days=2"
    )

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,pressure_msl,relativehumidity_2m"
        f"&past_days=2"
    )


    aq_resp = requests.get(aq_url).json()
    print("AQ RESPONSE:", aq_resp)
    weather_resp = requests.get(weather_url).json()
    print("WEATHER RESPONSE:", weather_resp)

    pm10 = aq_resp["hourly"]["pm10"]
    temperature = weather_resp["hourly"]["temperature_2m"]
    pressure = weather_resp["hourly"]["pressure_msl"]
    humidity = weather_resp["hourly"]["relativehumidity_2m"]

    rows =[]

    for t,p,h,pm in zip(temperature, pressure, humidity, pm10):
        if None not in (t,p,h,pm):
            rows.append([t,p,h,pm])
    # make sure have enough 24h lookback        
    if len(rows) < LOOKBACK:
        raise ValueError(f"Not enough data: only {len(rows)} valid hours")
    

    return rows[-LOOKBACK:]


def predict_pm25 (lat, lon):
    rows = fetch_last_24h(lat, lon)
    X = np.array(rows, dtype=np.float32)
    X_scaled = feature_scaler.transform(X) #(24 rows,4 features)
    X_input = X_scaled.reshape(1, LOOKBACK, 4) #(1 prediction request, 24 hours, 4 features)
    pred_scaled = model.predict(X_input, verbose = 0)
    pred = target_scaler.inverse_transform(pred_scaled)

    return round(float(pred[0][0]), 2)

if __name__ == "__main__":
    result = predict_pm25(32.1, -81.2)
    print(f"Predicted PM2.5: {result} µg/m³")