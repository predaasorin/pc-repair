import random
import string
from fastapi import FastAPI, Depends, HTTPException
from app.schemas import CreareReparatieRaspuns,CreareReparatie, RaspunsReparatie
from app.database import SesiuneLocala
from sqlalchemy.orm import Session
from app.modele import Clienti,Reparatii, StatusReparatie

app = FastAPI()


def get_db():
    db = SesiuneLocala()
    try:
        yield db
    finally:
        db.close()

def genereaza_cod_urmarire() -> str:

    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))

    return f"RPR-{part1}-{part2}"

@app.get("/health")
def health():
    return {
        "message": "Salut"
    }

@app.post("/api/reparatii", response_model=CreareReparatieRaspuns)
def creare_reparatie(reparatie_input:CreareReparatie, db: Session = Depends(get_db)):
    client = db.query(Clienti).filter(Clienti.telefon == reparatie_input.telefon).first()

    if not client:
        client = Clienti(
            nume = reparatie_input.nume,
            telefon = reparatie_input.telefon,
            email = reparatie_input.email
        )
        db.add(client)
        db.commit()
        db.refresh(client)


    cod_nou = genereaza_cod_urmarire()

    while db.query(Reparatii).filter(Reparatii.cod_urmarire == cod_nou).first():
        cod_nou = genereaza_cod_urmarire()


    reparatie = Reparatii(
        cod_urmarire = cod_nou,
        id_client = client.id,
        tip_dispozitiv = reparatie_input.tip_dispozitiv.value,
        brand = reparatie_input.brand,
        model = reparatie_input.model,
        numar_serie = reparatie_input.numar_serie,
        descrierea_problemei = reparatie_input.descrierea_problemei,
        data_predare = reparatie_input.data_predare,
        status_reparatie = StatusReparatie.PRIMIT
    )

    db.add(reparatie)
    db.commit()

    return {"tracking_code": cod_nou}


@app.get("/api/reparatii/{cod_urmarire}", response_model= RaspunsReparatie)
def informatii_reparatie(cod_urmarire: str, db: Session = Depends(get_db)):

    reparatie = db.query(Reparatii).filter(Reparatii.cod_urmarire == cod_urmarire).first()

    if not reparatie:
        raise HTTPException(status_code=404, detail="Reparația nu a fost găsită.")

    evenimente_client = []
    for ev in reparatie.evenimente:
        if ev.este_public == True:
            evenimente_client.append(ev)

    return{
        "cod_urmarire":reparatie.cod_urmarire,
        "status_reparatie":reparatie.status_reparatie.value,
        "tip_dispozitiv":reparatie.tip_dispozitiv.value,
        "brand":reparatie.brand,
        "model":reparatie.model,
        "descrierea_problemei":reparatie.descrierea_problemei,
        "data_predare":reparatie.data_predare,
        "data_estimata_finalizata":reparatie.data_estimata_finalizata,
        "creat_la":reparatie.creat_la,
        "actualizat_la":reparatie.actualizat_la,
        "evenimente":evenimente_client,
        "oferte":reparatie.oferte
    }