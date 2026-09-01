import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL nu a fost gasit in fisierul .env!")

# print(f"{DATABASE_URL}@*#&&!+++++++++++++++++++++++++++++++++++++++++++++")
motor = create_engine(DATABASE_URL)


SesiuneLocala = sessionmaker( bind = motor)

Baza = declarative_base()

def get_db():
    db = SesiuneLocala()
    try:
        yield db
    finally:
        db.close()