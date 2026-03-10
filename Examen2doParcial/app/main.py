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

reservas = [
    {"id": 1, "nombre": "Sergio Alvarez Matias", "edad": 21},
    {"id": 2, "nombre": "Ali", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]

#Modelo de datos para crear reserva
class crear_reserva(BaseModel):
    id: int = Field(..., ej="1")
    nombre: str = Field(..., min_length=6,ej="Sergio Alvarez Matias")
    fecha: str = Field(..., ej="2026-01-01")
    hora: str = Field(..., ej="19:00")
    numero_personas: int = Field(..., ej=4)

@app.get("/v1/reservas/", tags=['HTTP CRUD'])
async def reservas():
    return {"total": len(reservas), "reservas": reservas}

@app.post("/v1/usuarios/", tags=['HTTP CRUD'], status_code=status.HTTP_201_CREATED)
async def crear_reserva(usuario: crear_reserva):
    for usr in reservas:
        if usr ["id"] == usuario.id:
            raise HTTPException(
                status_code=400, 
                detail="El id ya existe"
            )
    
    reservas.append(usuario)
    return {"mensaje": "Reserva Creada", "Reserva": usuario}

#Modelo de datos para listar reservas
class listar_reservas(BaseModel):
    id: int = Field(..., ej="1"),
    nombre: str = Field(..., ej="Sergio Alvarez Matias")
    fecha: str = Field(..., ej="2026-10-03")
    hora: str = Field(..., ej="02:55")
    personas: int = Field(..., min_length=1, max_length=10, ej="2")
    estado: str = Field(..., ej="Pendiente")

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

#Modelo de datos para cancelar reservas
@app.delete("/v1/usuarios/{usuario_id}", tags=['HTTP CRUD'])
async def cancelar_reserva(reserva_id: int):
    "Elimina reserva de la lista."
    for i, usr in enumerate(reservas):
        if usr["id"] == reserva_id:
            usuario_eliminado = reservas.pop(i)
            return {"mensaje": "Reserva cancelada", "reserva": usuario_eliminado}
    
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

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
