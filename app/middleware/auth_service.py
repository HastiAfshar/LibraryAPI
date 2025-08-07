from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from datetime import datetime, timedelta
import os
from dotenv import  load_dotenv


load_dotenv()

security = HTTPBearer()


ACCESS_TOKEN_EXP = int(os.getenv("ACCESS_TOKEN_EXP"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(user_id: int, role: str):
        
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXP)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token


def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user_id": payload.get("user_id"), "role": payload.get("role")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")



