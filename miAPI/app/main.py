from fastapi import FastAPI
from app.data import usuario as usuarioDB
from app.router import usuario,misc
from app.data.db import engine

usuarioDB.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title= "Mi Primer API",
    description= "Sergio Alvarez Matias",
    version= "1.0"
)

app.include_router(usuario.router)
app.include_router(misc.misc)