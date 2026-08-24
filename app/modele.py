from app.database import Baza
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Date, Boolean,Numeric
from sqlalchemy.sql import func
import enum
from sqlalchemy.orm import relationship


class TipDispozitiv(enum.Enum):
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
    ALL_IN_ONE = "ALL_IN_ONE"
    ALTUL = "ALTUL"

class StatusReparatie(enum.Enum):
    PRIMIT = "PRIMIT"
    IN_LUCRU = "IN_LUCRU"
    IN_DIAGNOSTICARE = "IN_DIAGNOSTICARE"
    OFERTA_IN_ASTEPTARE = "OFERTA_IN_ASTEPTARE"
    ASTEPTARE_PIESE = "ASTEPTARE_PIESE"
    PREGATIT_PENTRU_RIDICARE = "PREGATIT_PENTRU_RIDICARE"
    RIDICAT = "RIDICAT"
    ANULAT = "ANULAT"


class Rol(enum.Enum):
    TEHNICIAN = "TEHNICIAN"
    ADMIN = "ADMIN"


class Clienti(Baza):
    __tablename__ = "clienti"

    id = Column(Integer, primary_key= True, index= True)
    nume = Column(String(120), nullable=False)
    telefon = Column(String(30),unique= True, index= True, nullable=False)
    email = Column(String(255), nullable= True)
    creat_la = Column(DateTime(timezone= True), server_default= func.now())

    reparatii = relationship("Reparatii", back_populates="client")

class Reparatii(Baza):

    __tablename__ = "reparatii"

    id = Column(Integer, primary_key= True, index= True)
    cod_urmarire= Column(String(16), unique= True, index= True, nullable= False)
    id_client = Column(Integer, ForeignKey("clienti.id"),index=True, nullable= False)
    tip_dispozitiv = Column(Enum(TipDispozitiv), nullable= False)
    brand = Column(String(60), nullable= False)
    model = Column(String(80), nullable= False)
    numar_serie = Column(String(80), nullable= True)
    descrierea_problemei = Column(Text, nullable= False)
    status_reparatie = Column(
        Enum(StatusReparatie),
        default= StatusReparatie.PRIMIT,
        index= True,
        nullable= False
    )
    data_predare = Column(Date, index= True, nullable= False)
    data_estimata_finalizata = Column(Date, nullable= True)
    creat_la = Column(DateTime(timezone=True), server_default=func.now())
    actualizat_la = Column(DateTime(timezone=True), onupdate=func.now())

    client = relationship("Clienti", back_populates="reparatii")
    evenimente = relationship("EvenimenteReparatie", back_populates="reparatie")
    oferte = relationship("OfertaPret", back_populates="reparatie")

class EvenimenteReparatie(Baza):

    __tablename__ = "evenimente_reparatie"

    id = Column(Integer, primary_key=True)
    id_reparatie = Column(Integer, ForeignKey("reparatii.id"), index=True, nullable=False)
    status_initial = Column(Enum(StatusReparatie), nullable=True)
    status_actualizat = Column(Enum(StatusReparatie),nullable=True)
    notita = Column(Text, nullable=True)
    este_public = Column(Boolean, default=False)
    autor = Column(String(120), nullable=True)
    creat_la = Column(DateTime(timezone=True), server_default=func.now(), index= True)

    reparatie = relationship("Reparatii", back_populates="evenimente")

class OfertaPret(Baza):

    __tablename__ = "oferta_pret"

    id = Column(Integer, primary_key= True)
    id_reparatie = Column(Integer, ForeignKey("reparatii.id"), index=True, nullable=False)
    cost_manopera = Column(Numeric(10, 2), nullable=False)
    cost_piese = Column(Numeric(10,2), nullable=False)
    descriere = Column(Text, nullable=False)
    trimis_la = Column(DateTime(timezone=True), nullable=True)
    aprobat_la = Column(DateTime(timezone=True), nullable=True)
    refuzat_la = Column(DateTime(timezone=True), nullable=True)
    creat_la = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    reparatie = relationship("Reparatii", back_populates="oferte")

class UtilizatoriAdmin(Baza):

    __tablename__ = "utilizatori_admin"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True,index=True, nullable=False)
    parola_criptata = Column(String(255),nullable= False)
    rol = Column(Enum(Rol), nullable= False)
    este_activ = Column(Boolean,default=True, nullable= False)
    creat_la = Column(DateTime(timezone=True), server_default=func.now(), index=True)