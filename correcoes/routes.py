from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import Correcao, CorrecaoInDB

router = APIRouter()

@router.get("/correcoes/")
async def list_correcoes():
    return await database.list_correcoes()

@router.get("/correcoes/redacao/{redacao_id}")
async def get_correcao_by_redacao(redacao_id: str):
    correcao = await database.get_correcao_by_redacao_id(redacao_id)
    if correcao:
        return correcao
    else:
        raise HTTPException(status_code=404, detail="Correcao não encontrada")

@router.get("/correcoes/{correcao_id}")
async def get_correcao(correcao_id: str):
    correcao = await database.get_correcao(correcao_id)
    if correcao:
        return correcao
    else:
        raise HTTPException(status_code=404, detail="Correcao não encontrada")

@router.post("/correcoes/")
async def create_correcao(correcao: Correcao = Body(...)):
    new_correcao = await database.create_correcao(correcao)
    return new_correcao

@router.put("/correcoes/{correcao_id}")
async def update_correcao(correcao_id: str, correcao: Correcao = Body(...)):
    return await database.update_correcao(correcao_id, correcao)

@router.delete("/correcoes/{correcao_id}")
async def delete_correcao(correcao_id: str):
    return await database.delete_correcao(correcao_id)
