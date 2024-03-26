from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status
import jwt
from pymongo import MongoClient
from .models import Token, User
from .database import ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES


client = MongoClient('mongodb+srv://root:root@projeto.hufetlu.mongodb.net/?retryWrites=true&w=majority&appName=projeto')
db = client["test"]
collection = db["users"]


router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(request: Request):
    form_data = await request.json()
    username = form_data.get("username")
    password = form_data.get("password")

    user = authenticate_user(collection, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "email": user.email, "nome":user.nome, "tipo": user.tipo, "turma": user.turma}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]


def verify_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login"))) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Rota protegida que requer o token para acesso
@router.get("/protected/")
async def protected_route(payload: dict = Depends(verify_token)):
    return {"message": "Rota protegida!", "payload": payload}
