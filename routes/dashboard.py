# routes/dashboard.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from services.database import (
    obtine_sarcini_din_db, 
    adauga_sarcina_db, 
    bifeaza_sarcina_db, 
    sterge_sarcina_db
)
from services.weather import obtine_coordonate_oras, obtine_vremea, obtine_prognoza
from services.currency import obtine_curs_valutar
from services.quote import obtine_citat_zilei
from services.holiday import obtine_urmatoarea_sarbatoare
from utils import salut, zile_saptamana_ro, luni_ro, zile_saptamana

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def radacina():
    return RedirectResponse("/home")

@router.get("/home")
def home(request: Request):
    acum = datetime.now()
    ora = acum.strftime("%H:%M")
    mesaj = salut(acum.hour)

    ziua_saptamanii = zile_saptamana_ro[acum.weekday()]
    data_curenta = f"{ziua_saptamanii}, {acum.day} {luni_ro[acum.month]} {acum.year}"

    sarcini_ordonate = obtine_sarcini_din_db()
    nume_oras_cautat = request.query_params.get("oras", "Iași")
    info_oras = obtine_coordonate_oras(nume_oras_cautat)

    curs_valutar = obtine_curs_valutar()
    citat_zilei = obtine_citat_zilei()
    urmatoarea_sarbatoare = obtine_urmatoarea_sarbatoare()

    try:
        data_vreme = obtine_vremea(info_oras["latitude"], info_oras["longitude"])
        data_prognoza = obtine_prognoza(info_oras["latitude"], info_oras["longitude"])
        ora_actualizarii = datetime.now().strftime("%H:%M")
        
        curent = data_vreme.get("current", {})
        vreme = {
            "name": info_oras["name"],
            "sys": {"country": info_oras.get("country", "")},
            "main": {
                "temp": curent.get("temperature_2m"),
                "humidity": curent.get("relative_humidity_2m"),
                "temp_min": data_prognoza.get("daily", {}).get("temperature_2m_min", [0])[0],
                "temp_max": data_prognoza.get("daily", {}).get("temperature_2m_max", [0])[0],
            },
            "wind": {"speed": curent.get("wind_speed_10m", 0) / 3.6},
            "weather": [{"description": "Vreme curentă", "icon": "01d"}]
        }
        
        daily = data_prognoza.get("daily", {})
        zile_forecast = daily.get("time", [])
        t_max = daily.get("temperature_2m_max", [])
        t_min = daily.get("temperature_2m_min", [])
        
        temperaturi_forecast = {}
        for i in range(1, min(6, len(zile_forecast))):
            data_zi = datetime.strptime(zile_forecast[i], "%Y-%m-%d")
            nume_zi = zile_saptamana[data_zi.weekday()][:3]
            temperaturi_forecast[nume_zi] = {
                "temp_max": round(t_max[i]) if t_max[i] is not None else 0,
                "temp_min": round(t_min[i]) if t_min[i] is not None else 0
            }
        eroare = None
    except Exception as e:
        vreme = None
        ora_actualizarii = "--:--"
        temperaturi_forecast = {}
        eroare = f"Eroare la obținerea vremii: {e}"

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "ora": ora,
            "ora_actualizarii": ora_actualizarii,
            "salut": mesaj,
            "vreme": vreme,
            "eroare": eroare,
            "oras": info_oras["name"],
            "temperaturi_forecast": temperaturi_forecast,
            "data_curenta": data_curenta,
            "sarcini": sarcini_ordonate,
            "curs_valutar": curs_valutar,
            "citat_zilei": citat_zilei,
            "urmatoarea_sarbatoare": urmatoarea_sarbatoare,
        },
    )

@router.post("/sarcini/adauga")
def adauga_sarcina(titlu: str = Form(...), prioritate: str = Form(...)):
    adauga_sarcina_db(titlu, prioritate)
    return RedirectResponse("/home", status_code=303)

@router.post("/sarcini/{sarcina_id}/bifeaza")
def bifeaza_sarcina(sarcina_id: int):
    bifeaza_sarcina_db(sarcina_id)
    return RedirectResponse("/home", status_code=303)

@router.post("/sarcini/{sarcina_id}/sterge")
def sterge_sarcina(sarcina_id: int):
    sterge_sarcina_db(sarcina_id)
    return RedirectResponse("/home", status_code=303)