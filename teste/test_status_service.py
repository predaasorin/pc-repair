from app.modele import StatusReparatie
from app.services.status_service import este_tranzitie_valida


def test_tranzitie_valida_primit_la_diagnosticare():

    rezultat = este_tranzitie_valida(StatusReparatie.PRIMIT, StatusReparatie.IN_DIAGNOSTICARE)
    assert rezultat == True

def test_tranzitie_invalida_primit_la_ridicat():

    rezultat = este_tranzitie_valida(StatusReparatie.PRIMIT, StatusReparatie.RIDICAT)
    assert  rezultat == False

def test_tranzitie_invalida_inapoi_din_anulat():

    rezultat = este_tranzitie_valida(StatusReparatie.ANULAT, StatusReparatie.IN_LUCRU)
    assert  rezultat == False

