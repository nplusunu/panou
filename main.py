# Initializarea aplicatiei FastAPI
# uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers import dashboard

app = FastAPI(title="Panou")

# Înregistrăm rutele din modularizare
app.include_router(dashboard.router)

@app.get("/style.css")
def stil():
    return FileResponse("templates/style.css")