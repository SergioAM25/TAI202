from pydantic import BaseModel, Field

class crear_usuario(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre: str = Field(...,min_length=0, max_length=50, example = "Juanita")
    edad: int = Field(...,ge=1, le=123, description= "Edad valida entre 1 y 123")