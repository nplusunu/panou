# Obtinerea informatiilor pentru prognoza meteo

from datetime import datetime
import requests
from config import CHEIE_OPEN_WEATHER

ZILE_SAPTAMANA = ["Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"]

def obtine_vremea(oras: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": oras,
        "appid": CHEIE_OPEN_WEATHER,
        "units": "metric",
        "lang": "ro",
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

def obtine_prognoza(oras: str):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": oras,
        "appid": CHEIE_OPEN_WEATHER,
        "units": "metric",
        "lang": "ro",
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

def calculeaza_temperatura(zile: dict):
    rezultate = {}
    for ziua, intervale in zile.items():
        # Folosim list comprehensions pentru eficiență și cod mai curat
        temperatura_minima = [x["main"]["temp_min"] for x in intervale]
        temperatura_maxima = [x["main"]["temp_max"] for x in intervale]
        
        media_minima = sum(temperatura_minima) / len(temperatura_minima)
        medie_maxima = sum(temperatura_maxima) / len(temperatura_maxima)
        
        rezultate[ziua] = {
            "temp_min": round(media_minima, 1),
            "temp_max": round(medie_maxima, 1),
        }
    return rezultate

def proceseaza_prognoza(prognoza_json):
    zile = {}
    for x in prognoza_json["list"]:
        data = datetime.strptime(x["dt_txt"], "%Y-%m-%d %H:%M:%S")
        ziua = ZILE_SAPTAMANA[data.weekday()]
        if ziua not in zile:
            zile[ziua] = []
        zile[ziua].append(x)
        
    temperaturi_forecast = calculeaza_temperatura(zile)
    # Returnăm doar următoarele 5 zile
    return dict(list(temperaturi_forecast.items())[1:6])