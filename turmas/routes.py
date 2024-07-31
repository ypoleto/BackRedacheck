from fastapi import APIRouter, HTTPException, Body, Query
from . import database
from typing import Optional
from .models import Turma, TurmaInDB

router = APIRouter()

@router.get("/turmas/")
async def list_turmas(professor_id: Optional[int] = Query(None)):
    return await database.list_turmas(professor_id=professor_id)

@router.get("/turmas/{turma_id}")
async def get_turma(turma_id: str):
    turma = await database.get_turma(turma_id)
    if turma:
        return turma
    else:
        raise HTTPException(status_code=404, detail="Turma not found")

@router.post("/turmas/")
async def create_turma(turma: Turma = Body(...)):
    new_turma = await database.create_turma(turma)
    return new_turma

@router.put("/turmas/{turma_id}")
async def update_turma(turma_id: str, turma: Turma = Body(...)):
    return await database.update_turma(turma_id, turma)

@router.delete("/turmas/{turma_id}")
async def delete_turma(turma_id: str):
    return await database.delete_turma(turma_id)
