# services/holiday.py
from datetime import datetime, date
import requests

def obtine_urmatoarea_sarbatoare():
    an_curent = datetime.now().year
    url = f"https://date.nager.at/api/v3/PublicHolidays/{an_curent}/RO"
    
    try:
        raspuns = requests.get(url, timeout=5)
        raspuns.raise_for_status()
        sarbatori = raspuns.json()
        
        azi = date.today()
        
        for s in sarbatori:
            data_sarbatoare = datetime.strptime(s.get("date"), "%Y-%m-%d").date()
            if data_sarbatoare >= azi:
                diferenta_zile = (data_sarbatoare - azi).days
                
                if diferenta_zile == 0:
                    text_zile = "azi"
                elif diferenta_zile == 1:
                    text_zile = "mâine"
                elif diferenta_zile == 2:
                    text_zile = "2 zile"
                else:
                    text_zile = f"{diferenta_zile} zile"
                
                zi = data_sarbatoare.day
                luni_ro_local = ["", "ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"]
                luna_nume = luni_ro_local[data_sarbatoare.month]
                
                return {
                    "nume": s.get("localName"),
                    "data": f"{zi} {luna_nume}",
                    "text_zile": text_zile
                }
    except Exception as e:
        print(f"Eroare preluare sărbători legale: {e}")
    
    return {
        "nume": "Crăciunul",
        "data": "25 decembrie",
        "text_zile": "curând"
    }