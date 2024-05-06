from typing import Optional
from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import UsersHasCidades, UsersHasCidadesInDB

router = APIRouter()

@router.get("/users_cidades/")
async def list_users_has_cidades(user_id: Optional[int] = None):
    if user_id is not None:
        return await database.list_users_has_cidades(user_id)
    else:
        return await database.list_users_has_cidades()

@router.get("/users_cidades/{users_has_cidades_id}")
async def get_user_has_cidades(users_has_cidades_id: int):
    turma = await database.get_user_has_cidades(users_has_cidades_id)
    if turma:
        return turma
    else:
        raise HTTPException(status_code=404, detail="UsersHasCidades not found")

@router.post("/users_cidades/")
async def create_user_has_cidades(user_has_cidades: UsersHasCidades = Body(...)):
    new_user_has_cidades = await database.create_user_has_cidade(user_has_cidades)
    return new_user_has_cidades

@router.put("/users_cidades/{users_has_cidades_id}")
async def update_user_has_cidades(users_has_cidades_id: int, users_has_cidades: UsersHasCidades = Body(...)):
    return await database.update_user_has_cidades(users_has_cidades_id, users_has_cidades)

@router.delete("/users_cidades/{users_has_cidades_id}")
async def delete_user_has_cidades(users_has_cidades_id: int):
    return await database.delete_user_has_cidades(users_has_cidades_id)
