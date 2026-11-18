# services/currency.py
import requests

def obtine_curs_valutar():
    url = "https://api.frankfurter.dev/v2/rates"
    params = {"base": "RON", "quotes": "EUR,USD,GBP"}
    try:
        raspuns = requests.get(url, params=params, timeout=5)
        raspuns.raise_for_status()
        date = raspuns.json()
        
        rates = {}
        data_actualizarii = "-"
        
        if isinstance(date, list) and len(date) > 0:
            for item in date:
                quote = item.get("quote")
                rate = item.get("rate")
                if quote and rate:
                    rates[quote] = round(1 / rate, 4)
                if "date" in item:
                    data_actualizarii = item.get("date")
        
        return {
            "EUR": rates.get("EUR", 4.9700),
            "USD": rates.get("USD", 4.6000),
            "GBP": rates.get("GBP", 5.8000),
            "data": data_actualizarii
        }
    except Exception as e:
        print(f"Eroare curs valutar: {e}")
        return {"EUR": 4.97, "USD": 4.60, "GBP": 5.80, "data": "Indisponibil"}