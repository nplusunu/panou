# services/quote.py
from datetime import datetime
import requests

cache_citat = {
    "data": None,
    "citat": "Cea mai mare glorie nu o obții atunci când nu cazi niciodată, ci atunci când te ridici după fiecare cădere.",
    "autor": "Confucius"
}

def obtine_citat_zilei():
    global cache_citat
    azi = datetime.now().strftime("%Y-%m-%d")

    if cache_citat["data"] == azi:
        return {
            "citat": cache_citat["citat"],
            "autor": cache_citat["autor"]
        }

    url = "https://zenquotes.io/api/today"
    try:
        raspuns = requests.get(url, timeout=5)
        raspuns.raise_for_status()
        date = raspuns.json()
        
        if isinstance(date, list) and len(date) > 0:
            citat_obj = date[0]
            cache_citat["data"] = azi
            cache_citat["citat"] = citat_obj.get("q", cache_citat["citat"])
            cache_citat["autor"] = citat_obj.get("a", cache_citat["autor"])
    except Exception as e:
        print(f"Eroare citat zilei: {e}")
    
    return {
        "citat": cache_citat["citat"],
        "autor": cache_citat["autor"]
    }