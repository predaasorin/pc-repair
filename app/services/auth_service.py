import os
import jwt
import bcrypt
from datetime import datetime,timedelta,timezone

SECRET_KEY = os.getenv("SECRET_KEY", "cheiesecreta")
ALGORITHM = "HS256"

def hash_parola(parola_clara: str) -> str:

    salt = bcrypt.gensalt()
    hash_byte = bcrypt.hashpw(parola_clara.encode('utf-8'), salt)

    return  hash_byte.decode('utf-8')


def verificare_parola (parola_clara: str, parola_hash: str) -> bool:

    return bcrypt.checkpw(parola_clara.encode('utf-8'), parola_hash.encode('utf-8'))

def creeaza_token_acces(date: dict, expira_in_minute: int = 60) -> str:

    pentru_encode = date.copy()
    expirare = datetime.now(timezone.utc) + timedelta(minutes=expira_in_minute)
    pentru_encode.update({"exp":expirare})

    token = jwt.encode(pentru_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token