from pydantic import BaseModel, Field

# Validacion de usuario
class crear_usuario(BaseModel):
    nombre: str = Field(...,min_length=0, max_length=50, example = "Juanita")
    edad: int = Field(...,ge=1, le=123, description= "Edad valida entre 1 y 123")