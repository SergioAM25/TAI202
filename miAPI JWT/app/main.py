from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI(title="miApiJWT")

# --- CONFIGURACIONES (Punto a) ---
SECRET_KEY = "secure pass" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 25 # (Punto b: Límite 30 min)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- GENERACIÓN DE TOKENS (Punto b) ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- VALIDACIÓN DE TOKENS (Punto c) ---
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")

# --- ENDPOINT PARA LOGUEARSE ---
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "cheko" and form_data.password == "123456":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Usuario o password incorrectos")

# --- PROTECCIÓN DE ENDPOINTS (Punto d) ---
@app.put("/v1/usuarios/{id}")
async def update_user(id: int, user_data: dict, token: str = Depends(get_current_user)):
    return {"message": "Usuario actualizado", "por": token}

@app.delete("/v1/usuarios/{id}")
async def delete_user(id: int, token: str = Depends(get_current_user)):
    return {"message": "Usuario eliminado", "por": token}