from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from services.air_quality import get_current_pm25
from services.db import add_subscriber

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

    value = get_current_pm25(lat, lon)
    return jsonify({
        "lat": lat,
        "lon": lon,
        "pm2_5": value
    })

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