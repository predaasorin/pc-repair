from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class TipDispozitiv(str, Enum):
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
    ALL_IN_ONE = "ALL_IN_ONE"
    ALTUL = "ALTUL"

#SCHEMA PENTRU CREARE (ce trimite clientul prin POST)
class CreareReparatie(BaseModel):

    nume: str = Field(..., max_length=120)
    telefon: str = Field(..., max_length=30)
    email: EmailStr | None = Field(None, max_length=255)
    tip_dispozitiv: TipDispozitiv
    brand: str = Field(..., max_length=60)
    model: str = Field(..., max_length=80)
    numar_serie: str | None = Field(None, max_length=80)
    descrierea_problemei: str
    data_predare: date

#SCHEMA PENTRU RASPUNSUL LA CREARE (ce primeste clientul la POST /api/repairs)
class CreareReparatieRaspuns(BaseModel):
    cod_urmarire: str

#SCHEMA PENTRU EVENIMENTELE PUBLICE (Timeline-ul vazut de client)
class EvenimentPublicRaspuns(BaseModel):
    status_actualizat: str | None = None
    notita: str | None = None
    creat_la: datetime

    class Config:
        from_attributes = True

# 4. SCHEMA PENTRU OFERTA DE PRET (Vazuta de client la GET /api/repairs/{code})
class OfertaPretPublicRaspuns(BaseModel):
    cost_manopera: Decimal
    cost_piese: Decimal
    descriere: str
    aprobat_la: datetime | None = None
    refuzat_la: datetime | None = None
    creat_la: datetime

    class Config:
        from_attributes = True


#SCHEMA PENTRU RASPUNSUL COMPLET LA STATUSUL PUBLIC (GET /api/repairs/{tracking_code})
class RaspunsReparatie(BaseModel):


    cod_urmarire: str
    status_reparatie: str
    data_predare: date
    data_estimata_finalizata: date | None
    creat_la: datetime
    actualizat_la: datetime | None = None

    evenimente: list[EvenimentPublicRaspuns] = []
    oferte_pret: list[OfertaPretPublicRaspuns] = []

    class Config:
        from_attributes = True

class ActualizareReparatie(BaseModel):

    status_reparatie: str | None = None
    data_estimata_finalizata: date | None = None
    descrierea_problemei: str | None = None


#Scheme pentru autentificare

class LoginAdmin(BaseModel):
    email: EmailStr
    parola: str

class RaspunsToken(BaseModel):
    access_token: str
    token_type: str

#scheme pentru  admin

class EvenimentAdmin(BaseModel):
    id: int
    status_initial: str | None = None
    status_actualizat: str | None = None
    notita:str | None = None
    este_public: bool
    creat_la: datetime

    class Config :
        from_attributes = True


class DetaliiReparatieAdmin(BaseModel):
    id: int
    cod_urmarire: str
    status_reparatie: str
    descrierea_problemei: str
    evenimente: list[EvenimentAdmin] = []
    brand: str
    model: str

    class Config:
        from_attributes = True


class ActualizareStatus(BaseModel):
    status_nou: str



class DispozitivReparatieAdmin(BaseModel):
    id: int
    cod_urmarire: str
    status_reparatie: str
    data_predare: date

    class Config:
        from_attributes = True

class PaginaReparatii(BaseModel):
    total: int
    pagina: int
    dimensiune_pagina: int
    reparatii: list[DispozitivReparatieAdmin]


#Calendar

class ZiDisponibila(BaseModel):
    data: date
    disponibil: bool
    locuri_libere: int

class RaspunsDisponibilitate(BaseModel):
    interval: list[ZiDisponibila]


#Oferta

class CreareOferta(BaseModel):
    cost_manopera: Decimal
    cost_piese: Decimal
    descriere: str


class RaspunsOfertaClient(BaseModel):
    decizie: str

class CreareNotita(BaseModel):
    notita: str
    este_public: bool = False

# Creare Tehnician

class CreareTehnician(BaseModel):
    email: EmailStr
    parola: str