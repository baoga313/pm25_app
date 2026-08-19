import requests
import pandas as pd

lat = 32.1
lon = -81.2

# Air quality API
aq_url = (
    f"https://air-quality-api.open-meteo.com/v1/air-quality"
    f"?latitude={lat}&longitude={lon}"
    f"&hourly=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
    f"&start_date=2024-01-01&end_date=2025-01-01"
)

# Weather API
weather_url = (
    f"https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={lat}&longitude={lon}"
    f"&hourly=temperature_2m,relativehumidity_2m,pressure_msl,windspeed_10m"
    f"&start_date=2024-01-01&end_date=2025-01-01"
)

aq_data = requests.get(aq_url).json()
weather_data = requests.get(weather_url).json()

df_aq = pd.DataFrame(aq_data["hourly"]).set_index("time")
df_weather = pd.DataFrame(weather_data["hourly"]).set_index("time")

df = df_aq.join(df_weather)
df.index = pd.to_datetime(df.index)
df = df.dropna(axis=1, how="all")
df = df.dropna()

print(f"Available columns: {list(df.columns)}")
print(f"Total rows: {len(df)}")
print("\n=== Correlation with PM2.5 ===")
correlation = df.corr()["pm2_5"].sort_values(ascending=False)
print(correlation.round(3))