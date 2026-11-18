# Initializarea aplicatiei FastAPI
# uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.responses import FileResponse
from services.database import init_db
from routes.dashboard import router as dashboard_router

app = FastAPI()

# Inițializăm baza de date la pornire
init_db()

# Înregistrăm rutele din dashboard
app.include_router(dashboard_router)

@app.get("/style.css")
def stil():
    return FileResponse("templates/style.css")