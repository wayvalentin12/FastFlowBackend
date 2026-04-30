from models import Usuario
from schemes import UsuarioCreate
from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from auth import get_current_user


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
@router.patch("/{id_user}")
async def update_user(id_user: int, usuario: UsuarioCreate, db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    user=db.query(Usuario).filter(Usuario.id == id_user,Usuario.negocio_id == current_user.negocio_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    update_data = usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(usuario, key, value)
    db.commit()
    db.refresh(user)
    return user