from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import User, UserInDB

router = APIRouter()

@router.get("/users/")
async def list_users():
    return await database.list_users()

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await database.get_user(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/users/")
async def create_user(user: User = Body(...)):
    new_user = await database.create_user(user)
    print('aaa', new_user)
    return new_user

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User = Body(...)):
    return await database.update_user(user_id, user)

@router.put("/users/{user_id}/change-password")
async def change_user_password(user_id: str, new_password: str = Body(...)):
    # Chama a função para atualizar a senha do usuário
    result = await database.update_user_password(user_id, new_password)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    return await database.delete_user(user_id)

