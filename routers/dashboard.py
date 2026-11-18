from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import requests

from services.vreme import obtine_vremea, obtine_prognoza, proceseaza_prognoza

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def salut(ora: int) -> str:
    if ora < 12:
        return "Buna dimineata!"
    elif ora < 18:
        return "Buna ziua!"
    else:
        return "Buna seara!"

@router.get("/")
def radacina():
    """Ruta / ne trimite direct la /home."""
    return RedirectResponse("/home")

@router.get("/home")
def home(request: Request):
    acum = datetime.now()
    ora = acum.strftime("%H:%M")
    mesaj = salut(acum.hour)
    oras = request.query_params.get("oras", "Bacău")
    
    vreme = None
    temperaturi_forecast = {}
    eroare = None

    try:
        vreme = obtine_vremea(oras)
        prognoza_json = obtine_prognoza(oras)
        temperaturi_forecast = proceseaza_prognoza(prognoza_json)
    except requests.exceptions.RequestException as e:
        eroare = f"Eroare la obținerea datelor meteo: {e}"

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "ora": ora,
            "salut": mesaj,
            "vreme": vreme,
            "eroare": eroare,
            "oras": oras,
            "temperaturi_forecast": temperaturi_forecast,
        },
    )