from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.rute import admin, auth, clienti, tehnician

app = FastAPI(title="PC Repair Shop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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