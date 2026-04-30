from sqlalchemy.orm import Session
from models import Categoria
from schemes import CategoriaCreate
from database import get_db
from fastapi import APIRouter, HTTPException, Depends
from auth import get_current_user
router=APIRouter()

@router.get("/")
async def all_categories(db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    return db.query(Categoria).filter(Categoria.negocio_id == current_user.negocio_id).all()
@router.get("/{id_category}")
async def specific_category(id_category: int ,db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    category= db.query(Categoria).filter(Categoria.id == id_category,Categoria.negocio_id == current_user.negocio_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Esta categoria no esta disponible")
    return category
@router.post("/")
async def create_category(categoria: CategoriaCreate,db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    new_category= Categoria(
        nombre_categoria=categoria.nombre_categoria,
        negocio_id=current_user.negocio_id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
@router.put("/{id_category}")
async def update_category(id_category: int, categoria: CategoriaCreate, db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    updated_category=db.query(Categoria).filter(Categoria.id == id_category,Categoria.negocio_id == current_user.negocio_id).first()
    if not updated_category:
        raise HTTPException(status_code=404, detail="Esta categoria no esta disponible")
    if categoria.nombre_categoria is not None:
        updated_category.nombre_categoria = categoria.nombre_categoria
    db.commit()
    db.refresh(updated_category)
    return updated_category
@router.delete("/{id_category}")
async def del_category(id_category: int, db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    category=db.query(Categoria).filter(Categoria.id == id_category,Categoria.negocio_id == current_user.negocio_id).first()
    if not category:
        raise HTTPException(status_code=404,detail="No fue posible encontrar la categoria")
    db.delete(category)
    db.commit()


