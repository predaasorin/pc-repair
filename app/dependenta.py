import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.auth_service import ALGORITHM, SECRET_KEY

security = HTTPBearer()

def verifica_token_angajat(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        rol = payload.get("rol")

        if payload.get("rol") not in ["ADMIN", "TEHNICIAN"]:
            raise HTTPException(status_code=403, detail="Nu ai drepturi de acces.")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirat, Te rugam sa te reloghezi")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalid")

def verifica_token_strict_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verifica_token_angajat(credentials)
    if payload.get("rol") != "ADMIN":
        raise HTTPException(status_code=403, detail="Actiune permisa strict administratorilor")
    return  payload
