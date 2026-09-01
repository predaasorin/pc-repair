from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.database import get_db
from app.dependenta import verificara_token_admin
from app.services import status_service
from app.schemas import DetaliiReparatieAdmin, ActualizareStatus, PaginaReparatii, OfertaPretPublicRaspuns, CreareOferta, CreareNotita, EvenimentAdmin
from app.modele import Reparatii, StatusReparatie, Clienti, OfertaPret,EvenimenteReparatie


ruta_admin = APIRouter(prefix="/api/admin/reparatii", tags=["Admin"])



@ruta_admin.get("/{id}",response_model=DetaliiReparatieAdmin)
def obtine_reparatie_admin(id: int, admin_data: dict = Depends(verificara_token_admin), db: Session = Depends(get_db)):

    reparatie = db.query(Reparatii).filter(Reparatii.id == id).first()

    if not reparatie:
        raise  HTTPException(status_code=404, detail="Reparatia nu a fost gasita")

    return reparatie


@ruta_admin.patch("/{id}/status")
def schimba_status_reparatie(
        id: int,
        status_input: ActualizareStatus,
        admin_data: dict = Depends(verificara_token_admin),
        db: Session = Depends(get_db)

):

    reparatie = db.query(Reparatii).filter(Reparatii.id == id).first()

    if not reparatie:
        raise HTTPException(status_code=404, detail="Reparatia nu a fost gasita")

    status_curent = reparatie.status_reparatie

    try:
        status_dorit = StatusReparatie[status_input.status_nou.upper()]

    except KeyError:
        raise HTTPException(status_code=400, detail="Statusul specificat nu exista")

    if not status_service.este_tranzitie_valida(status_curent, status_dorit):
        raise HTTPException(status_code=409, detail=f"Tranzitie ilegala de la {status_curent.value} la {status_dorit.value}")

    reparatie.status_reparatie = status_dorit
    db.commit()

    return {"message": "Status actualizat cu succes"}

@ruta_admin.get("", response_model=PaginaReparatii)
def listeaza_reparatii_admin(
        status: Optional[str] = None,
        q: Optional[str] = None,
        pagina: int = 1,
        marime_pagina: int = 10,
        admin_data: dict = Depends(verificara_token_admin),
        db: Session = Depends(get_db)
):
    query = db.query(Reparatii).join(Clienti)

    if status:
        query = query.filter(Reparatii.status_reparatie == status.upper())

    if q:
        termen = f"%{q}%"
        query = query.filter(
            or_(
                Reparatii.cod_urmarire.ilike(termen),
                Clienti.nume.ilike(termen),
                Clienti.telefon.ilike(termen)

            )
        )

    total_rezultate = query.count()

    offset = (pagina - 1) * marime_pagina

    reparatii = query.offset(offset).limit(marime_pagina).all()

    return {
        "total": total_rezultate,
        "pagina": pagina,
        "dimensiune_pagina": marime_pagina,
        "reparatii": reparatii
    }

@ruta_admin.post("/{reparatie_id}/oferta", response_model= OfertaPretPublicRaspuns)
def creaza_oferta_pret(
        reparatie_id:int,
        oferta_in:CreareOferta,
        admin_data: dict = Depends(verificara_token_admin),
        db: Session = Depends(get_db)

):
    reparatie = db.query(Reparatii).filter(Reparatii.id == reparatie_id).first()

    if not reparatie:
        raise HTTPException(status_code=404, detail="Reparatia nu a fost gasita")

    status_dorit = StatusReparatie.OFERTA_IN_ASTEPTARE
    if not status_service.este_tranzitie_valida(reparatie.status_reparatie, status_dorit):
        raise HTTPException(status_code=409, detail=f"Tranzitie ilegala de la {reparatie.status_reparatie.value} la {status_dorit.value}. Nu se poate adauga oferta" )


    oferta_noua = OfertaPret(
        id_reparatie = reparatie_id,
        cost_manopera = oferta_in.cost_manopera,
        cost_piese = oferta_in.cost_piese,
        descriere = oferta_in.descriere,
    )

    db.add(oferta_noua)

    reparatie.status_reparatie = status_dorit

    db.commit()
    db.refresh(oferta_noua)

    return oferta_noua


@ruta_admin.post("/{id}/evenimente", response_model=EvenimentAdmin)
def adaugare_notita_tehnician(
        id: int,
        notita_in: CreareNotita,
        admin_data: dict = Depends(verificara_token_admin),
        db: Session = Depends(get_db)
):
    reparatie = db.query(Reparatii).filter(Reparatii.id == id).first()

    if not reparatie:
        raise HTTPException(status_code=404, detail="Reparatia nu a fost gasita")

    autor_email = admin_data.get("subiect", "Tehnician")

    eveniment_nou = EvenimenteReparatie(
        id_reparatie = id,
        status_initial = reparatie.status_reparatie,
        status_actualizat = reparatie.status_reparatie,
        notita = notita_in.notita,
        este_public = notita_in.este_public,
        autor = autor_email
    )

    db.add(eveniment_nou)
    db.commit()
    db.refresh(eveniment_nou)

    return eveniment_nou