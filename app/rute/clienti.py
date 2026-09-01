from time import timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.modele import Clienti, Reparatii, StatusReparatie, EvenimenteReparatie
from app.schemas import CreareReparatieRaspuns, CreareReparatie, RaspunsReparatie, RaspunsOfertaClient
from app.utils import genereaza_cod_urmarire
from datetime import  date, datetime,timezone
from app.services import disponibilitate_service

ruta_clienti = APIRouter(prefix= "/api/reparatii", tags=["Clienti"])



@ruta_clienti.get("/disponibilitate", response_model=schemas.RaspunsDisponibilitate)
def verifica_disponibilitatea(
        de_la_data: date,
        pana_la_data: date,
        db: Session = Depends(get_db)
):

    if de_la_data > pana_la_data:
        raise HTTPException(status_code=400, detail= "Data 'de la data' trebuie sa fie inainte de 'pana la data'. ")

    if (pana_la_data - de_la_data).days > 60:
        raise  HTTPException(status_code=400 , detail="Intervalul maxim permis este de 60 de zile")

    return disponibilitate_service.afla_disponibilitatea(db, de_la_data, pana_la_data)



@ruta_clienti.post("", response_model=CreareReparatieRaspuns)
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

    if reparatie_input.data_predare.weekday() == 6:
        raise  HTTPException(status_code=400, detail="Magazinul este inchis duminica. Te rugam sa alegi  o alta zi pentru predare")

    programari_existende = db.query(Reparatii).filter(Reparatii.data_predare == reparatie_input.data_predare).count()

    if programari_existende >= 3:
        raise HTTPException(status_code=400, detail="Ne pare rau, capacitatea maxima de 3 echipamente pe zi  a fost atinsa")

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


@ruta_clienti.post("/{cod_urmarire}/oferte/raspuns")
def raspunde_la_oferta(
        cod_urmarire: str,
        raspuns: RaspunsOfertaClient,
        db: Session = Depends(get_db)
):
    reparatie = db.query(Reparatii).filter(Reparatii.cod_urmarire == cod_urmarire).first()

    if not reparatie:
        raise HTTPException(status_code=404, detail="Reparatia nu a fost gasita")

    if reparatie.status_reparatie != StatusReparatie.OFERTA_IN_ASTEPTARE:
        raise  HTTPException(status_code=400, detail="Aceasta reparatie nu asteapta  un raspuns la oferta")

    oferta_activa = None
    for oferta in reparatie.oferte:
        if oferta.aprobat_la is None and oferta.refuzat_la is None:
            oferta_activa = oferta
            break

    if not oferta_activa:
        raise HTTPException(status_code=404, detail="Nu s-a gasit nici o oferta in asteptare")

    timp_curent = datetime.now(timezone.utc)
    status_vechi = reparatie.status_reparatie
    if raspuns.decizie == "acceptat":
        oferta_activa.aprobat_la = timp_curent
        reparatie.status_reparatie = StatusReparatie.IN_LUCRU
        mesaj_notita = "Clientul a acceptat oferta de pret. Reparatia va incepe"
    elif raspuns.decizie == "refuzat":
        oferta_activa.refuzat_la = timp_curent
        reparatie.status_reparatie = StatusReparatie.PREGATIT_PENTRU_RIDICARE
        mesaj_notita = "Clientul a refuzat oferta de pret. Dispozitivul este pregatit pentru  a fi ridicat nereparat."

    else:
        raise HTTPException(status_code=400, detail="Decizie invalida, alege intre acceptat sau refuzat")

    eveniment_nou = EvenimenteReparatie(
        id_reparatie = reparatie.id,
        status_initial = status_vechi,
        status_actualizat = reparatie.status_reparatie,
        notita = mesaj_notita,
        este_public = True,
        autor = "Client"
    )

    db.add(eveniment_nou)
    db.commit()

    return {"mesaj":"Raspunsul a fost inregistrat cu succes",
            "status_nou": reparatie.status_reparatie.value
            }



@ruta_clienti.get("/{cod_urmarire}", response_model= RaspunsReparatie)
def informatii_reparatie(cod_urmarire: str, db: Session = Depends(get_db)):

    reparatie = db.query(Reparatii).filter(Reparatii.cod_urmarire == cod_urmarire).first()

    if not reparatie:
        raise HTTPException(status_code=404, detail="Reparatia nu a fost gasita.")

    evenimente_client = []
    for ev in reparatie.evenimente:
        if ev.este_public == True:
            evenimente_client.append({
                "status_actualizat": ev.status_actualizat.value if ev.status_actualizat else None,
                "notita": ev.notita,
                "creat_la": ev.creat_la
            })

    oferte_client = []
    for oferta in reparatie.oferte:
        oferte_client.append({
            "cost_manopera": oferta.cost_manopera,
            "cost_piese": oferta.cost_piese,
            "descriere": oferta.descriere,
            "aprobat_la": oferta.aprobat_la,
            "refuzat_la": oferta.refuzat_la,
            "creat_la": oferta.creat_la
        })



    return{
        "cod_urmarire": reparatie.cod_urmarire,
        "status_reparatie": reparatie.status_reparatie.value,
        "tip_dispozitiv": reparatie.tip_dispozitiv.value,
        "brand": reparatie.brand,
        "model": reparatie.model,
        "descrierea_problemei": reparatie.descrierea_problemei,
        "data_predare": reparatie.data_predare,
        "data_estimata_finalizata": reparatie.data_estimata_finalizata,
        "creat_la": reparatie.creat_la,
        "actualizat_la": reparatie.actualizat_la,
        "evenimente": evenimente_client,
        "oferte_pret": oferte_client
    }
