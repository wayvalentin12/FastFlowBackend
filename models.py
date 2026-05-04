from sqlalchemy import Column, String, Integer, ForeignKey,Float,JSON, DateTime, Numeric,Boolean
from sqlalchemy.sql import func
from database import Base

class Negocio(Base):
    __tablename__ ="negocios"
    id=Column(Integer, autoincrement=True, primary_key=True)
    nombre_negocio=Column(String(50), nullable=False)

class Usuario(Base):
    __tablename__ ="usuarios"

    id= Column(Integer, autoincrement=True, primary_key=True)
    nombre=Column(String(50), nullable=False)
    email=Column(String(100),nullable=False)
    password=Column(String(300), nullable=False)
    negocio_id=Column(Integer,ForeignKey("negocios.id"),nullable=False)


class Categoria(Base):
    __tablename__="categorias"
    id=Column(Integer,autoincrement=True,primary_key=True)
    nombre_categoria=Column(String(50),nullable=False)
    negocio_id=Column(Integer,ForeignKey("negocios.id"),nullable=False)


class Producto(Base):
    __tablename__="productos"
    id=Column(Integer,autoincrement=True,primary_key=True)
    nombre= Column(String(50), nullable=False, unique=True)
    categoria_id= Column(Integer,ForeignKey("categorias.id"),nullable=False )
    precio= Column(Float, nullable=False)
    cantidad= Column(Integer, nullable=False)
    min_cantidad= Column(Integer, nullable=False)
    negocio_id=Column(Integer,ForeignKey("negocios.id"),nullable=False)

class Venta(Base):
    __tablename__="ventas"
    id=Column(Integer,autoincrement=True,primary_key=True)
    fecha=Column(DateTime, nullable=False)
    nombre_cliente= Column(String(50),nullable=False)
    producto=Column(String(50),ForeignKey("productos.nombre"),nullable=False)
    cantidad=Column(Integer,nullable=False)
    precio=Column(Float, nullable=False)
    total=Column(Float,nullable=False)
    negocio_id=Column(Integer,ForeignKey("negocios.id"),nullable=False)

class VentaTotalDia(Base):
    __tablename__ = "venta_total_dia"

    id = Column(Integer, primary_key=True, index=True)
    negocio_id = Column(Integer, ForeignKey("negocios.id"),nullable=False)
    fecha_apertura = Column(DateTime(timezone=True), server_default=func.now())
    fecha_cierre = Column(DateTime(timezone=True), nullable=True)
    estado = Column(String(10), default="abierta")
    resumen = Column(JSON, nullable=True)
    total_dia = Column(Numeric(10,2), nullable=True)
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    email=Column(String(100),nullable=False)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    fecha_expiracion=Column(DateTime(timezone=True), nullable=False)
    revocado=Column(Boolean, default=False)

   

    