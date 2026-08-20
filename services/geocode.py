import requests

def get_city_name(lat, lon):
    url = (f"https://nominatim.openstreetmap.org/reverse"
           f"?lat={lat}&lon={lon}&format=json")
    # requirement of nominatim to identify the application (avoid blocked with 403)
    headers = {"User-Agent": "PM25AirQualityApp/1.0"}

    try:
        response = requests.get(url, headers = headers, timeout = 5)
        data= response.json()
        address = data.get("address", {})
        city = (
            address.get("city")
            or address.get("town") 
            or address.get("village") 
            or address.get("county")
        )
        state = address.get("state")

        if city and state:
            return f"{city}, {state}"
        elif city:
            return city
        else:
            return f"{lat:.2f}, {lon:.2f}"

    except Exception as e:
        return f"{lat:.2f}, {lon:.2f}"




