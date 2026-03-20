from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. Definimos la URL de conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5432/miapi_db"
)

#2. Creamos el motor de conexión
engine = create_engine(DATABASE_URL)

#3. Preparamos el gestionador de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#4. Base declarativa del modelo
Base = declarative_base()

#5. Obtener sesiones de cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()