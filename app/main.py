from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.rute import tehnician, auth, clienti, admin

app = FastAPI(title="PC Repair Shop API")
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")


app.include_router(auth.ruta_login)
app.include_router(clienti.ruta_clienti)
app.include_router(tehnician.ruta_tehnician)
app.include_router(admin.ruta_admin)


@app.get("/health")
def health():
    return {
        "message": "Sistemul este online!"
    }