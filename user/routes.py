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
    return new_user

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User = Body(...)):
    return await database.update_user(user_id, user)

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    return await database.delete_user(user_id)
