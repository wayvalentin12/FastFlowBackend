from auth import create_token, verify_psw
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
from models import Usuario

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
    print(token)
    return {"access_token": token, "token_type": "bearer"}