from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import Redacao, RedacaoInDB

router = APIRouter()

@router.get("/redacoes/")
async def list_redacoes(user_id: int):
    return await database.list_redacoes(user_id)

@router.get("/redacoes/{redacao_id}")
async def get_redacao(redacao_id: str):
    redacao = await database.get_redacao(redacao_id)
    if redacao:
        return redacao
    else:
        raise HTTPException(status_code=404, detail="Redacao não encontrada")

@router.post("/redacoes/")
async def create_redacao(redacao: Redacao = Body(...)):
    new_redacao = await database.create_redacao(redacao)
    return new_redacao

@router.put("/redacoes/{redacao_id}")
async def update_redacao(redacao_id: str, redacao: Redacao = Body(...)):
    return await database.update_redacao(redacao_id, redacao)

@router.delete("/redacoes/{redacao_id}")
async def delete_redacao(redacao_id: str):
    return await database.delete_redacao(redacao_id)
