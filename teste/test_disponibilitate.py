from datetime import date
from app.services.disponibilitate_service import afla_disponibilitatea
from app.modele import Reparatii, Clienti, StatusReparatie, TipDispozitiv

def test_locuri_libere_zi_goala(db):

    zi_test = date(2026, 10, 5)

    rezultat = afla_disponibilitatea(db, zi_test, zi_test)

    interval = rezultat["interval"]
    assert len(interval) == 1
    assert interval[0]["data"] == zi_test
    assert interval[0]["locuri_libere"] == 3
    assert interval[0]["disponibil"] == True


def test_disponibilitate_cu_reparatii(db):
    zi_test = date(2026, 10, 5)

    client_test = Clienti(nume="Client Test", telefon="0700000000", email="test@test.ro")
    db.add(client_test)
    db.commit()
    db.refresh(client_test)

    reparatie1 = Reparatii(
        cod_urmarire="TEST-01", id_client=client_test.id, tip_dispozitiv=TipDispozitiv.LAPTOP,
        brand="Asus", model="ROG", descrierea_problemei="Test 1", status_reparatie=StatusReparatie.PRIMIT,
        data_predare=zi_test
    )
    reparatie2 = Reparatii(
        cod_urmarire="TEST-02", id_client=client_test.id, tip_dispozitiv=TipDispozitiv.LAPTOP,
        brand="Dell", model="XPS", descrierea_problemei="Test 2", status_reparatie=StatusReparatie.PRIMIT,
        data_predare=zi_test
    )
    db.add(reparatie1)
    db.add(reparatie2)
    db.commit()

    rezultat = afla_disponibilitatea(db, zi_test, zi_test)

    assert rezultat["interval"][0]["locuri_libere"] == 1
    assert rezultat["interval"][0]["disponibil"] == True


def test_disponibilitate_duminica(db):
    zi_duminica = date(2026, 10, 11)  

    rezultat = afla_disponibilitatea(db, zi_duminica, zi_duminica)

    assert rezultat["interval"][0]["locuri_libere"] == 0
    assert rezultat["interval"][0]["disponibil"] == False