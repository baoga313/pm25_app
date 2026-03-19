from flask import Flask, jsonify, request
from services.air_quality import get_current_pm25

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/api/pm25')
def pm25():
    lat = request.args.get("lat", type = float)
    lon = request.args.get("lon", type = float)

    if lat is None or lon is None:
        return jsonify({"error": "Please provide lat and lon"}), 400

    value = get_current_pm25(lat, lon)
    return jsonify({
        "lat": lat,
        "lon": lon,
        "pm2_5": value
    })

if __name__ == '__main__':
    app.run(debug=True)