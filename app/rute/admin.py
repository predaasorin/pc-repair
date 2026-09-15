from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.modele import UtilizatoriAdmin, Rol
from app.schemas import CreareTehnician
from app.services.auth_service import hash_parola
from app.dependenta import verifica_token_strict_admin

ruta_admin = APIRouter(prefix="/api/admin", tags=["Admin"])

@ruta_admin.post("/tehnicieni")
def adauga_tehinician(
        date_tehnician: CreareTehnician,
        admin_data: dict = Depends(verifica_token_strict_admin),
        db: Session = Depends(get_db)
    ):

    if db.query(UtilizatoriAdmin).filter(UtilizatoriAdmin.email == date_tehnician.email).first():
        raise HTTPException(status_code=400, detail="Acest email este deja inregistrat")

    tehnician_nou = UtilizatoriAdmin(
        email = date_tehnician.email,
        parola_criptata = hash_parola(date_tehnician.parola),
        rol = Rol.TEHNICIAN,
        este_activ = True
    )

    db.add(tehnician_nou)
    db.commit()
    return {"mesaj": "Tehnician creat cu succes!"}