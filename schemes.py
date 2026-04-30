from enum import nonmember
from time import timezone
from pydantic import BaseModel
from datetime import date
from typing import Optional

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
class RegisterCreate(UsuarioCreate):
    nombre_negocio: str

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
    fecha: date
    nombre_cliente: str
    producto: str
    cantidad: int
    precio: float
    total: float
class CategoriaCreate(BaseModel):
    nombre_categoria: str
