from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as dbUsuario

router= APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios(db:Session = Depends(get_db)):
    queryUsuarios = db.query(dbUsuario).all()
    return {
        "status": "200", 
        "total": len(queryUsuarios), 
        "usuarios": queryUsuarios
        }
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP: crear_usuario, db:Session = Depends(get_db)):
    nuevoU = dbUsuario(nombre = usuarioP.nombre, edad = usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)

    return {
        "mensaje": "Usuario Creado", 
        "Usuario": usuarioP
        }

#PUT, PATCH Y DELETE 
    
@router.put("/{usuario_id}")
async def actualizar_usuario_completo(usuario_id: int, usuario_actualizado: dict):
    for indice, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios[indice] = usuario_actualizado
            return {"mensaje": "Usuario actualizado", "datos": usuarios[indice]}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.patch("/{usuario_id}")
async def actualizar_usuario_parcial(usuario_id: int, datos_parciales: dict):
    "Modifica solo los campos enviados."
    for usr in usuarios:
        if usr["id"] == usuario_id:
            usr.update(datos_parciales)
            return {"mensaje": "Usuario actualizado parcialmente", "usuario": usr}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.delete("/{usuario_id}")
async def eliminar_usuario(usuario_id: int, usuarioAuth:str= Depends(verificar_peticion)):

    "Elimina al usuario de la lista."
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuario_eliminado = usuarios.pop(i)
            return {"mensaje": f"Usuario eliminado por {usuarioAuth}"}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")