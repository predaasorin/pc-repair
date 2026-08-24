from app.modele import StatusReparatie


TRANZITII_FINALE = {
    StatusReparatie.PRIMIT : {StatusReparatie.IN_DIAGNOSTICARE, StatusReparatie.ANULAT},
    StatusReparatie.IN_DIAGNOSTICARE : {StatusReparatie.OFERTA_IN_ASTEPTARE, StatusReparatie.ANULAT},
    StatusReparatie.OFERTA_IN_ASTEPTARE : {StatusReparatie.IN_LUCRU,StatusReparatie.PREGATIT_PENTRU_RIDICARE, StatusReparatie.ANULAT},
    StatusReparatie.IN_LUCRU : {StatusReparatie.ASTEPTARE_PIESE, StatusReparatie.PREGATIT_PENTRU_RIDICARE, StatusReparatie.ANULAT},
    StatusReparatie.ASTEPTARE_PIESE : {StatusReparatie.IN_LUCRU, StatusReparatie.ANULAT},
    StatusReparatie.PREGATIT_PENTRU_RIDICARE : {StatusReparatie.RIDICAT, StatusReparatie.ANULAT},
    StatusReparatie.RIDICAT : set(),
    StatusReparatie.ANULAT : set()

}


def este_tranzitie_valida(status_curent: StatusReparatie, status_dorit:StatusReparatie) -> bool:

    if status_dorit == StatusReparatie.ANULAT and status_curent not in [StatusReparatie.RIDICAT, StatusReparatie.ANULAT]:
        return True

    stari_permise = TRANZITII_FINALE.get(status_curent, set())
    return status_dorit in stari_permise