from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum
from decimal import Decimal


class TipDispozitiv(str, Enum):
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
    ALL_IN_ONE = "ALL_IN_ONE"
    ALTUL = "ALTUL"

#SCHEMA PENTRU CREARE (ce trimite clientul prin POST)
class CreareReparatie(BaseModel):

    nume: str = Field(..., max_length=120)
    telefon: str = Field(..., max_length=30)
    email: Optional[EmailStr] = Field(None, max_length=255)
    tip_dispozitiv: TipDispozitiv
    brand: str = Field(..., max_length=60)
    model: str = Field(..., max_length=80)
    numar_serie: Optional[str] = Field(None, max_length=80)
    descrierea_problemei: str
    data_predare: date

#SCHEMA PENTRU RĂSPUNSUL LA CREARE (ce primește clientul la POST /api/repairs)
class CreareReparatieRaspuns(BaseModel):
    tracking_code: str

#SCHEMA PENTRU EVENIMENTELE PUBLICE (Timeline-ul văzut de client)
class EvenimentPublicRaspuns(BaseModel):
    status_actualizat: Optional[str] = None
    notita: Optional[str] = None
    creat_la: datetime

    class Config:
        orm_mode = True

# 4. SCHEMA PENTRU OFERTA DE PREȚ (Văzută de client la GET /api/repairs/{code})
class OfertaPretPublicRaspuns(BaseModel):
    cost_manopera: Decimal
    cost_piese: Decimal
    descriere: str
    aprobat_la: Optional[datetime] = None
    refuzat_la: Optional[datetime] = None
    creat_la: datetime

    class Config:
        orm_mode = True


#SCHEMA PENTRU RĂSPUNSUL COMPLET LA STATUSUL PUBLIC (GET /api/repairs/{tracking_code})
class RaspunsReparatie(BaseModel):


    cod_urmarire: str
    status_reparatie: str
    data_predare: date
    data_estimata_finalizata: Optional[date]
    creat_la: datetime
    actualizat_la: Optional[datetime] = None

    evenimente: list[EvenimentPublicRaspuns] = []
    oferte_pret: list[OfertaPretPublicRaspuns] = []

    class Config:
        orm_mode = True

class ActualizareReparatie(BaseModel):

    status_reparatie: Optional[str] = None
    data_estimata_finalizata: Optional[date] = None
    descrierea_problemei: Optional[str] = None
