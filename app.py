from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from services.air_quality import get_history_pm25
from services.db import add_subscriber
from services.geocode import get_city_name
from services.predictor import predict_pm25

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/api/pm25')
def pm25():
    lat = request.args.get("lat", type = float)
    lon = request.args.get("lon", type = float)

    if lat is None or lon is None:
        return jsonify({"error": "Please provide your location"}), 400
    city = get_city_name(lat,lon)
    value = get_history_pm25(lat, lon)
    current = value[-1]
    return jsonify({
        "lat": lat,
        "lon": lon,
        "pm2_5": current,
        "city": city
    })

@app.route('/api/predict')
def predict():
    lat = request.args.get("lat", type=float)  
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Please provide your location"}), 400

    try:
        prediction  = predict_pm25(lat, lon)
        return jsonify({
            "lat": lat,
            "lon": lon,
            "predicted_pm25": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)},500)


@app.route('/api/subscribe', methods = ["POST"])
def subscribe():
    data = request.get_json()
    email = data.get('email')
    lat = data.get('lat')
    lon = data.get('lon')

    if email is not None:
        # check if the user input is an email format
        if "@" not in email or "." not in email.split("@")[-1]:
            return jsonify({"message": "Invalid email format"}), 400
        add_subscriber(email, lat, lon)
        return jsonify({"message": "Subscribed successfully!"})
    else:
        return jsonify({"message": "Email is required"}), 400
    

if __name__ == '__main__':
    app.run(debug=True)