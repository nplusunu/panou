# services/weather.py
import requests

def obtine_coordonate_oras(nume_oras):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": nume_oras, "count": 1, "language": "ro", "format": "json"}
    try:
        raspuns = requests.get(url, params=params, timeout=5)
        raspuns.raise_for_status()
        date = raspuns.json()
        if "results" in date and len(date["results"]) > 0:
            locatie = date["results"][0]
            return {
                "name": locatie.get("name"),
                "country": locatie.get("country", ""),
                "latitude": locatie.get("latitude"),
                "longitude": locatie.get("longitude")
            }
    except Exception:
        pass
    return {"name": "Iași", "country": "România", "latitude": 47.1585, "longitude": 27.6014}

def obtine_vremea(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m",
        "timezone": "auto"
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

def obtine_prognoza(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()