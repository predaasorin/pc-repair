from datetime import date, timedelta
from sqlalchemy.orm import  Session
from sqlalchemy import  func
from app import modele


NUMAR_MAXIM_LUCRARI_PE_ZI = 3

def afla_disponibilitatea(db:Session, inceput_data:date, sfarsit_data:date):


    zile_rezultat = []

    reparatii_programate = db.query(
        modele.Reparatii.data_predare,
        func.count(modele.Reparatii.id).label('numar')
    ).filter(
        modele.Reparatii.data_predare >= inceput_data,
        modele.Reparatii.data_predare <= sfarsit_data
    ).group_by(modele.Reparatii.data_predare).all()

    programari_pe_zi = {rezultat.data_predare: rezultat.numar for rezultat in reparatii_programate}

    ziua_curenta = inceput_data

    while ziua_curenta <= sfarsit_data:
        locuri_ocupate = programari_pe_zi.get(ziua_curenta, 0)
        locuri_libere = NUMAR_MAXIM_LUCRARI_PE_ZI - locuri_ocupate

        este_duminica =  ziua_curenta.weekday() == 6

        disponibil =  not este_duminica and locuri_libere > 0

        zile_rezultat.append({
            "data": ziua_curenta,
            "disponibil": disponibil,
            "locuri_libere" : 0  if este_duminica else max(0, locuri_libere)
        })

        ziua_curenta += timedelta(days=1)

    return {"interval": zile_rezultat}