import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Baza

SQL_ALCHEMY_DATABASE_URL = "sqlite:///./baza_de_date.db"

motor = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestareSesiuneLocala = sessionmaker(autocommit = False, autoflush = False, bind = motor)


@pytest.fixture(scope="function")
def db():

    Baza.metadata.create_all(bind = motor)
    sesiune_db = TestareSesiuneLocala()

    try:
        yield sesiune_db

    finally:
        sesiune_db.close()
        Baza.metadata.drop_all(bind = motor)