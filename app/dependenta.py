from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.services.auth_service import SECRET_KEY,ALGORITHM


security = HTTPBearer()

def verificara_token_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        rol = payload.get("rol")

        if rol!= "ADMIN":
            raise HTTPException(status_code=403, detail="nu ai drepturi de administrator")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirat, Te rugam sa te reloghezi")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalid")
