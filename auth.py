from fastapi import security
from models import Usuario, RefreshToken
from datetime import timezone
from typing_extensions import deprecated
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
EXPIRE_ACCESS_TOKEN=int(os.getenv("EXPIRE_ACCESS_TOKEN",30))
ALGORITHM=os.getenv("ALGORITHM")
EXPIRE_REFRESH_TOKEN=int(os.getenv("EXPIRE_REFRESH_TOKEN",7))

security= HTTPBearer()
psw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def hash_psw(password: str):
    return psw_context.hash(password)
def verify_psw(plained_psw: str, hashed_psw: str):
    return psw_context.verify(plained_psw, hashed_psw)

def create_refresh_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(days=EXPIRE_REFRESH_TOKEN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_refresh_token(token: str,db:Session= Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        negocio_id=payload.get("negocio_id")
        if not email or not negocio_id:
            raise HTTPException(status_code=401, detail="El usuario no esta autorizado")
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.revocado == False
        ).first()
        if not db_token:
            raise HTTPException(status_code=401, detail="Refresh Token invalido")
        return email,negocio_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido")

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_ACCESS_TOKEN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      email = payload.get("sub")
      negocio_id=payload.get("negocio_id")
      if not email or not negocio_id:
        raise HTTPException(status_code=401, detail="El usuario no esta autorizado")
      return email,negocio_id
    except JWTError:
      raise HTTPException(status_code=401, detail="Token invalido")
def get_current_user(credentials: HTTPAuthorizationCredentials= Depends(security),db:Session= Depends(get_db)):
  email, negocio_id = verify_token(credentials.credentials)
  user = db.query(Usuario).filter(Usuario.email == email, Usuario.negocio_id == negocio_id).first()
  if not user:
      raise HTTPException(status_code=401, detail="Usuario no encontrado")
  return user
