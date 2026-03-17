from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

router= APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios():
    return {"total": len(usuarios), "usuarios": usuarios}
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr ["id"] == usuario.id:
            raise HTTPException(
                status_code=400, 
                detail="El id ya existe"
            )
    
    usuarios.append(usuario)
    return {"mensaje": "Usuario Creado", "Usuario": usuario}

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