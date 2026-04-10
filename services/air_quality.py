import requests

def get_history_pm25(lat, lon):
    url = f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5&past_days=1'
    response = requests.get(url)
    data = response.json()
    all_values = data["hourly"]["pm2_5"]

    readings = [v for v in all_values if v is not None]

    return readings[-24:]