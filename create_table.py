from database import Base, engine
import models

Base.metadata.drop_all(bind=engine)
print("Tablas eliminadas de forma exitosa")

Base.metadata.create_all(bind=engine)
print("TABLA CREADA")
