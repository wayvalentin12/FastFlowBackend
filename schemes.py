from enum import nonmember
from time import timezone
from pydantic import BaseModel
from datetime import date
from typing import Optional
from datetime import datetime 

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    email: str | None = None
    password: str | None = None
class RegisterCreate(UsuarioCreate):
    nombre_negocio: str
    rol: str

class UsuarioResponse(UsuarioCreate):
    nombre: str
    email: str
class ProductoCreate(BaseModel):
    nombre: str
    categoria_id: int
    precio: float
    cantidad: int
    min_cantidad: int
class ProductoUpdate(BaseModel):
    nombre: str | None = None
    categoria_id: int | None = None
    precio: float | None = None
    cantidad: int | None = None
    min_cantidad: int | None = None
class VentaCreate(BaseModel):
    fecha: datetime 
    nombre_cliente: str
    producto: str
    cantidad: int
    precio: float
    total: float
class CategoriaCreate(BaseModel):
    nombre_categoria: str

class VentaTotalDiaResponse(BaseModel):
    id: int
    negocio_id: int
    fecha_apertura: datetime
    fecha_cierre: Optional[datetime]
    estado: str
    resumen: Optional[dict]
    total_dia: Optional[float]

    class Config:
        from_attributes = True

class VentaResumenDiaResponse(BaseModel):
    estado: str
    resumen: Optional[dict]
    total_dia: Optional[float]

