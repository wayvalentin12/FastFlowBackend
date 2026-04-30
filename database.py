from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")

engine= create_engine(SUPABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    conection = engine.connect()
    print("Conectado a la base de datos!")
    conection.close()
except Exception as e:
    print("error:", e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()