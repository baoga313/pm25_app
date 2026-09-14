from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS # type: ignore
from services.air_quality import get_history_pm25
from services.db import add_subscriber
from services.geocode import get_city_name
from services.predictor import predict_pm25
from services.scheduler import start_scheduler
from services.email_service import send_welcome
import re
import os

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
app = Flask(__name__, static_folder="frontend/dist", static_url_path="")
CORS(app)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

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
        return jsonify({"error": str(e)}),500


@app.route('/api/subscribe', methods = ["POST"])
def subscribe():
    data = request.get_json()
    email = data.get('email')
    lat = data.get('lat')
    lon = data.get('lon')
    threshold = data.get('threshold')

    if threshold is None:
        threshold = 35.0
    try:
        threshold = float(threshold)
    except(TypeError, ValueError):
        return jsonify({"message": "Invalid threshold"}), 400
    # check if any of user input is valid
    if threshold <= 0 or threshold > 500:
        return jsonify({"message": "Threshold must be between 0 and 500"}), 400

    if lat is None or lon is None:
        return jsonify({"message": "Location is required"}), 400
    
    if email is not None:
        # check if the user input is an email format
        if not EMAIL_RE.match(email):
            return jsonify({"message": "Invalid email format"}), 400
        city = get_city_name(lat,lon)
        add_subscriber(email, lat, lon, threshold)
        send_welcome(email, threshold, city)
        return jsonify({"message": "Subscribed successfully!"})
    else:
        return jsonify({"message": "Email is required"}), 400
    

if __name__ == '__main__':
    print("STARTING SCHEDULER...")
    start_scheduler()
    print("SCHEDULER STARTED, LAUNCHING FLASK...")
    port = int(os.environ.get("PORT", 5000))
    print(f"BINDING TO PORT {port}...")
    app.run(host="0.0.0.0", port=port)