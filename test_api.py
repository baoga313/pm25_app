from services.air_quality import get_current_pm25, get_history_pm25

# OpenWeatherMap current
owm = get_current_pm25(10.8231, -106.6297)
print(f"OpenWeatherMap: {owm}")

# Open-Meteo latest reading
history = get_history_pm25 (10.8231, -106.6297)
open_meteo = history[-1]
print(f"Open-Meteo: {open_meteo}")

print(f"Difference: {abs(owm - open_meteo):.2f} µg/m³")