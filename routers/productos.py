from fastapi import APIRouter,Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from models import Producto, Categoria
from schemes import ProductoCreate, ProductoUpdate
from auth import  get_current_user
from sqlalchemy import func
router=APIRouter()

@router.get("/")
async def all_products(db: Session=Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Producto).filter(Producto.negocio_id == current_user.negocio_id).all()
    
@router.post("/")
async def create_product(producto: ProductoCreate, db: Session=Depends(get_db), current_user = Depends(get_current_user)):
    new_product= Producto(
        nombre=producto.nombre,categoria_id=producto.categoria_id,precio=producto.precio
        ,cantidad=producto.cantidad,min_cantidad=producto.min_cantidad,negocio_id=current_user.negocio_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.patch("/{producto_id}")
async def update_product(producto_id: int, producto: ProductoUpdate, db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    db_product = db.query(Producto).filter(Producto.negocio_id == current_user.negocio_id, Producto.id == producto_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product
@router.delete("/{id_producto}")
async def del_product(id_producto: int,db: Session=Depends(get_db), current_user = Depends(get_current_user)):
    producto=db.query(Producto).filter(Producto.id == id_producto,Producto.negocio_id == current_user.negocio_id).first()
    db.delete(producto)
    db.commit()
    return producto
@router.get("/low-stock",response_model=list[ProductoCreate])
async def products_low_stock(db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    product=db.query(Producto).filter(Producto.cantidad <= Producto.min_cantidad,Producto.negocio_id == current_user.negocio_id).all()
    if not product:
        return []
    return product
@router.get("/valor-inventario")
async def stock_value(db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    total_stock = db.query(func.sum(Producto.cantidad * Producto.precio)).filter(Producto.negocio_id == current_user.negocio_id).scalar()
    return {"valor_total_inventario": total_stock or 0}
@router.get("/categorias")
async def category(db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    return db.query(Categoria).filter(Categoria.negocio_id == current_user.negocio_id).all()
@router.get("/categorias/{id_categoria}")
async def products_categories(id_categoria: int,db: Session=Depends(get_db), current_user = Depends(get_current_user)):
    categoria=db.query(Categoria).filter(Categoria.id == id_categoria, Categoria.negocio_id == current_user.negocio_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="No se pudo encontrar este producto")
    return db.query(Producto).filter(Producto.categoria_id == categoria.id, Producto.negocio_id == current_user.negocio_id).all()
