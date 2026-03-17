from fastapi import FastAPI
from app.router import usuario,misc

app = FastAPI(
    title= "Mi Primer API",
    description= "Sergio Alvarez Matias",
    version= "1.0"
)

app.include_router(usuario.router)
app.include_router(misc.misc)