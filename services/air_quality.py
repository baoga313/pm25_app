import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Load variable from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_current_pm25 (lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    pm25 = data["list"][0]["components"]["pm2_5"]
    return pm25