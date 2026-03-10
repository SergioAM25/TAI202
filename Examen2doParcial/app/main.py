#Crear reserva, listar reserva, consultar ID, confirmar reserva, cancelar reserva
#Nombre cliente minimo 6 caracteres, fecha reserva futura entre 8:00 am y 10:00 pm, numero personas entre 1 y 10, no permitir reservas en domingos
#Rutas protegidas con admin y contraseña: rest123 (listar reservas y cancelar citas)

from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional 
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title= "API de Sistema de Rservas de Restaurante",
    description= "Sergio Alvarez Matias",
    version= "1.0"
)

class crear_reserva(BaseModel):
    nombre: str = Field(..., ej="Sergio Alvarez Matias")
    fecha: str = Field(..., ej="2026-01-01")
    hora: str = Field(..., ej="19:00")
    numero_personas: int = Field(..., ej=4)

class reserva(crear_reserva):
    id: int = Field(..., ej=1)
    estado: str = Field(..., ej="pendiente")

security = HTTPBasic()
def verificar_credenciales(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "rest123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )

reservas = []
id_reserva = 1

class listar_reservas(BaseModel):
    id: int
    nombre: str
    fecha: str
    hora: str
    personas: int
    estado: str

    