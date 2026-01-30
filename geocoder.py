import requests
from config import MAPBOX_TOKEN

def geocode_location(place: str):
    """
    Convert place name -> (lat, lng)
    """
    try:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{place}.json"
        params = {
            "access_token": MAPBOX_TOKEN,
            "country": "IN",
            "limit": 1
        }

        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        if data.get("features"):
            lng, lat = data["features"][0]["center"]
            return lat, lng

    except Exception as e:
        print(f"Geocoding error for {place}: {e}")

    return None, None
