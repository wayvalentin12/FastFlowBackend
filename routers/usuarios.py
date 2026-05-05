from models import Usuario
from schemes import UsuarioUpdate
from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from auth import get_current_user, hash_psw


router = APIRouter()

@router.get("/")
async def all_users(db: Session=Depends(get_db)):
    return db.query(Usuario).all()
@router.get("/{id_user}")
async def specific_user(id_user: int ,db: Session=Depends(get_db)):
    user=db.query(Usuario).filter(Usuario.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="No fue posible encontrar el usuario")
    return user

@router.delete("/{id_user}")
async def del_user(id_user: int ,db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    user=db.query(Usuario).filter(Usuario.id == id_user,Usuario.negocio_id == current_user.negocio_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="No fue posible encontrar el usuario")
    db.delete(user)
    db.commit()
@router.patch("/")
async def update_user(usuario: UsuarioUpdate, db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    user=db.query(Usuario).filter(Usuario.id == current_user.id, Usuario.negocio_id == current_user.negocio_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    update_data = usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password" and value:
            value = hash_psw(value)
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user