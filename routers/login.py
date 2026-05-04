from auth import create_token, verify_psw, verify_refresh_token,create_refresh_token, EXPIRE_REFRESH_TOKEN
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
from models import Usuario,RefreshToken
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

EXPIRE_REFRESH_TOKEN = int(os.getenv("EXPIRE_REFRESH_TOKEN", 7))

router=APIRouter()
@router.post("/")
async def login_user(user: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    userdb = db.query(Usuario).filter(Usuario.email == user.username).first()
    if not userdb:
        raise HTTPException(status_code=404, detail="Nombre de usuario incorrecto")
    password= verify_psw(user.password,userdb.password)
    if not password:
        raise HTTPException(status_code=404, detail="Contraseña incorrecta")
    token = create_token({"sub": userdb.email, "negocio_id": userdb.negocio_id})
    refresh_token = create_refresh_token({"sub": userdb.email, "negocio_id": userdb.negocio_id})
    db_refresh_token=RefreshToken(
        token=refresh_token,
        email=userdb.email,
        negocio_id=userdb.negocio_id,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(days=EXPIRE_REFRESH_TOKEN),
        revocado=False
    )
    db.add(db_refresh_token)
    db.commit()
    return {"access_token": token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/refresh")
async def create_new_refresh_token(token: str, db: Session=Depends(get_db)):
    email, negocio_id = verify_refresh_token(token,db)
    new_token = create_token({"sub": email, "negocio_id": negocio_id})
    return {"access_token": new_token, "token_type": "bearer"}

@router.post("/logout")
async def logout_user(token: str, db: Session=Depends(get_db)):
    db_refresh_token=db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not db_refresh_token:
        raise HTTPException(status_code=404, detail="Token invalido")
    db_refresh_token.revocado=True
    db.commit()
    return {"message": "Sesión cerrada exitosamente"}