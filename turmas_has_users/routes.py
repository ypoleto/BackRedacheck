from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import TurmaHasUsers, TurmaHasUsersInDB

router = APIRouter()

@router.get("/turmas_users/")
async def list_turmas_has_users():
    return await database.list_turmas_has_users()

@router.get("/turmas_users/{turmas_has_users_id}")
async def get_turma_has_users(turmas_has_users_id: int):
    turma = await database.get_turma_has_users(turmas_has_users_id)
    if turma:
        return turma
    else:
        raise HTTPException(status_code=404, detail="TurmaHasUsers not found")

@router.post("/turmas_users/")
async def create_turma_has_users(turma_has_users: TurmaHasUsers = Body(...)):
    new_turma_has_users = await database.create_turma_has_user(turma_has_users)
    return new_turma_has_users

@router.put("/turmas_users/{turmas_has_users_id}")
async def update_turma_has_users(turmas_has_users_id: int, turmas_has_users: TurmaHasUsers = Body(...)):
    return await database.update_turma_has_users(turmas_has_users_id, turmas_has_users)

@router.delete("/turmas_users/{turmas_has_users_id}")
async def delete_turma_has_users(turmas_has_users_id: int):
    return await database.delete_turma_has_users(turmas_has_users_id)
