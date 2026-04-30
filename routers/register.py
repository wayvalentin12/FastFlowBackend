from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from models import Usuario,Negocio
from auth import hash_psw
from schemes import RegisterCreate


router=APIRouter()
@router.post("/",status_code=201)
async def register_user(user: RegisterCreate, db: Session=Depends(get_db)):
    userdb=db.query(Usuario).filter(Usuario.email == user.email).first()
    if userdb:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    negocio= Negocio(
        nombre_negocio=user.nombre_negocio
    )
    db.add(negocio)
    db.flush()
    

    new_user = Usuario(
        nombre=user.nombre,
        email=user.email,
        password=hash_psw(user.password),
        negocio_id=negocio.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario creado exitosamente", "user":new_user}