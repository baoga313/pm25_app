from services.air_quality import get_current_pm25

lat = 44.9365
lon = 26.0201

pm25 = get_current_pm25(lat, lon)
print(f"Current PM2.5: {pm25} µg/m³")