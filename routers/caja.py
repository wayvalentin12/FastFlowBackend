from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import VentaTotalDia, Venta
from datetime import datetime
from auth import get_current_user

router = APIRouter()


@router.post("/abrir")
async def abrir_caja(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    caja_abierta = db.query(VentaTotalDia).filter(
        VentaTotalDia.negocio_id == current_user.negocio_id,
        VentaTotalDia.estado == "abierta"
    ).first()

    if caja_abierta:
        raise HTTPException(status_code=400, detail="Ya hay una caja abierta")

    nueva_caja = VentaTotalDia(negocio_id=current_user.negocio_id)
    db.add(nueva_caja)
    db.commit()
    db.refresh(nueva_caja)
    return {"mensaje": "Caja abierta exitosamente", "caja_id": nueva_caja.id, "fecha_apertura": nueva_caja.fecha_apertura}


@router.get("/estado")
async def estado_caja(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    caja = db.query(VentaTotalDia).filter(
        VentaTotalDia.negocio_id == current_user.negocio_id,
        VentaTotalDia.estado == "abierta"
    ).first()

    if not caja:
        return {"abierta": False}

    return {
        "abierta": True,
        "caja_id": caja.id,
        "fecha_apertura": caja.fecha_apertura
    }


@router.get("/ventas-dia")
async def ventas_del_dia(current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    caja = db.query(VentaTotalDia).filter(
        VentaTotalDia.negocio_id == current_user.negocio_id,
        VentaTotalDia.estado == "abierta"
    ).first()

    if not caja:
        raise HTTPException(status_code=404, detail="No hay caja abierta")

    ventas = db.query(Venta).filter(
        Venta.negocio_id == current_user.negocio_id,
        Venta.fecha >= caja.fecha_apertura
    ).all()

    resumen = {}
    for v in ventas:
        if v.producto not in resumen:
            resumen[v.producto] = {
                "cantidad": 0,
                "precio_unitario": float(v.precio),
                "total": 0.0
            }
        resumen[v.producto]["cantidad"] += v.cantidad
        resumen[v.producto]["total"] += float(v.total)

    total_dia = round(sum(r["total"] for r in resumen.values()), 2)

    return {
        "productos": resumen,
        "total_dia": total_dia,
        "fecha_apertura": caja.fecha_apertura
    }


@router.post("/cerrar")
async def cerrar_caja(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    caja = db.query(VentaTotalDia).filter(
        VentaTotalDia.negocio_id == current_user.negocio_id,
        VentaTotalDia.estado == "abierta"
    ).first()

    if not caja:
        raise HTTPException(status_code=404, detail="No hay caja abierta")

    ventas = db.query(Venta).filter(
        Venta.negocio_id == current_user.negocio_id,
        Venta.fecha >= caja.fecha_apertura
    ).all()

    resumen = {}
    for v in ventas:
        if v.producto not in resumen:
            resumen[v.producto] = {
                "cantidad": 0,
                "precio_unitario": float(v.precio),
                "total": 0.0
            }
        resumen[v.producto]["cantidad"] += v.cantidad
        resumen[v.producto]["total"] += float(v.total)

    total_dia = round(sum(r["total"] for r in resumen.values()), 2)

    caja.resumen = resumen
    caja.total_dia = total_dia
    caja.fecha_cierre = datetime.now()
    caja.estado = "cerrada"

    db.commit()
    db.refresh(caja)

    return {
        "mensaje": "Caja cerrada exitosamente",
        "resumen": resumen,
        "total_dia": total_dia,
        "fecha_apertura": caja.fecha_apertura,
        "fecha_cierre": caja.fecha_cierre
    }

@router.get("/historial")
async def historial_cajas(current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    cajas = db.query(VentaTotalDia).filter(
        VentaTotalDia.negocio_id == current_user.negocio_id,
        VentaTotalDia.estado == "cerrada"
    ).order_by(VentaTotalDia.fecha_cierre.desc()).all()
    return cajas
