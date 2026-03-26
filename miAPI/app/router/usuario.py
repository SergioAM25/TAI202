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
async def ruta_crear_usuario(usuarioP: crear_usuario, db:Session = Depends(get_db)):
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
async def actualizar_usuario_completo(usuario_id: int, usuario_actualizado: crear_usuario, db: Session = Depends(get_db)):
    # 1. Buscar el usuario en la base de datos por ID 
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # 2. Actualizar todos los campos 
    usuario_db.nombre = usuario_actualizado.nombre
    usuario_db.edad = usuario_actualizado.edad
    
    db.commit()
    db.refresh(usuario_db)
    return {"mensaje": "Usuario actualizado", "datos": usuario_db}


@router.patch("/{usuario_id}")
async def actualizar_usuario_parcial(usuario_id: int, datos_parciales: dict, db: Session = Depends(get_db)):
    # 1. Buscar el usuario
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # 2. Actualizar solo los campos presentes en el diccionario
    for key, value in datos_parciales.items():
        if hasattr(usuario_db, key):
            setattr(usuario_db, key, value)
    
    db.commit()
    db.refresh(usuario_db)
    return {"mensaje": "Usuario actualizado parcialmente", "usuario": usuario_db}


@router.delete("/{usuario_id}")
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db), usuarioAuth: str = Depends(verificar_peticion)):
    # 1. Buscar el usuario
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # 2. Eliminar el registro de la base de datos 
    db.delete(usuario_db)
    db.commit()
    
    return {"mensaje": f"Usuario con ID {usuario_id} eliminado por {usuarioAuth}"}