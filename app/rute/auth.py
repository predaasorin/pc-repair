from fastapi import APIRouter, Depends, HTTPException
from app.database import  get_db
from sqlalchemy.orm import Session
from app.schemas import RaspunsToken, LoginAdmin
from app.modele import UtilizatoriAdmin
from app.services import auth_service

ruta_login = APIRouter(prefix="/api/auth", tags=["Autentificare"])


@ruta_login.post("/login", response_model= RaspunsToken)
def login_admin(date_login: LoginAdmin, db: Session = Depends(get_db)):

    utilizator = db.query(UtilizatoriAdmin).filter(UtilizatoriAdmin.email == date_login.email).first()

    if not utilizator or not auth_service.verificare_parola(date_login.parola, utilizator.parola_criptata):
        raise HTTPException(status_code=401, detail= "Email sau Parola  incorecte")

    token = auth_service.creeaza_token_acces(
        date = {"subiect":utilizator.email, "rol": utilizator.rol.value}
    )

    return {"access_token": token, "token_type": "bearer"}


@ruta_login.post("/logout")
def logout_admin():
    return {"message": "Delogare cu succes"}