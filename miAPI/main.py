#Importaciones
from fastapi import FastAPI
import asyncio

#Instancia del servidor
app = FastAPI()
async def holamundo():
    return{"mensaje":"Hola Mundo FastAPI"}

#Endpoints
@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Bienvenido a FastAPI",
        "estatus":"200"
        }