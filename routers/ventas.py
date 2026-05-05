from models import Venta, Producto
from schemes import VentaCreate
from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from auth import get_current_user
router=APIRouter()

@router.get("/")
async def all_sales(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return db.query(Venta).filter(Venta.negocio_id == current_user.negocio_id).all()
@router.post("/", status_code=201)
async def add_sale(venta: VentaCreate,db: Session=Depends(get_db),current_user = Depends(get_current_user)):

    product = db.query(Producto).filter(Producto.id == venta.producto_id, Producto.negocio_id == current_user.negocio_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if product.cantidad < venta.cantidad:
        raise HTTPException(status_code=400,
         detail=f"Stock insuficiente, cantidad actual del producto: {product.cantidad}")

    new_sale= Venta(
        fecha=venta.fecha,
        nombre_cliente=venta.nombre_cliente
        ,producto=product.nombre
        ,cantidad=venta.cantidad
        ,precio=venta.precio
        ,total=venta.total
        ,negocio_id=current_user.negocio_id
    )
    
    product.cantidad -= venta.cantidad

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale
@router.get("/{id_sale}")
async def specific_sale(id_sale: int ,db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    sale = db.query(Venta).filter(Venta.id == id_sale,Venta.negocio_id == current_user.negocio_id).first()
    if not sale:
        raise HTTPException(status_code=404,detail="No fue posible encontrar la venta")
    return sale
