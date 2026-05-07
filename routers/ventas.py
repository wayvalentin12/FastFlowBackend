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
    sales_created = []
    
    for item in venta.items:
        product = db.query(Producto).filter(Producto.id == item.producto_id, Producto.negocio_id == current_user.negocio_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Producto con id {item.producto_id} no encontrado")

        if product.cantidad < item.cantidad:
            raise HTTPException(status_code=400,
             detail=f"Stock insuficiente para {product.nombre}, cantidad actual: {product.cantidad}")

        new_sale = Venta(
            fecha=venta.fecha,
            nombre_cliente=venta.nombre_cliente,
            producto=product.nombre,
            cantidad=item.cantidad,
            precio=item.precio,
            total=item.total,
            negocio_id=current_user.negocio_id
        )
        
        product.cantidad -= item.cantidad
        db.add(new_sale)
        sales_created.append(new_sale)

    db.commit()
    for sale in sales_created:
        db.refresh(sale)
        
    return sales_created
@router.get("/{id_sale}")
async def specific_sale(id_sale: int ,db: Session=Depends(get_db),current_user = Depends(get_current_user)):
    sale = db.query(Venta).filter(Venta.id == id_sale,Venta.negocio_id == current_user.negocio_id).first()
    if not sale:
        raise HTTPException(status_code=404,detail="No fue posible encontrar la venta")
    return sale
