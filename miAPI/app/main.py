from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/programador/{id}")
async def obligatorio(id: int, nombre: str):
    return {
        "perfil": "Programador (Vista Docs)",
        "id": id,
        "nombre": nombre
    }

@app.get("/usuario")
async def opcional(username: str = "Invitado", premium: bool = False):
    return {
        "perfil": "Usuario Final (Vista Redoc)",
        "username": username,
        "es_premium": premium
    }

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {"mensaje": "Bienvenido a FastAPI", "estatus": "200"}

