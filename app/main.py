from fastapi import FastAPI
from app.rute import auth, clienti, admin

app = FastAPI(title="PC Repair Shop API")


app.include_router(auth.ruta_login)
app.include_router(clienti.ruta_clienti)
app.include_router(admin.ruta_admin)


@app.get("/health")
def health():
    return {
        "message": "Sistemul este online!"
    }