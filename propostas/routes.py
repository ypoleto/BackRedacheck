from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import Proposta, PropostaInDB

router = APIRouter()

@router.get("/propostas/")
async def list_propostas():
    return await database.list_propostas()

@router.get("/propostas/{proposta_id}")
async def get_proposta(proposta_id: str):
    proposta = await database.get_proposta(proposta_id)
    if proposta:
        return proposta
    else:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")

@router.post("/propostas/")
async def create_proposta(proposta: Proposta = Body(...)):
    new_proposta = await database.create_proposta(proposta)
    return new_proposta

@router.put("/propostas/{proposta_id}")
async def update_proposta(proposta_id: str, proposta: Proposta = Body(...)):
    return await database.update_proposta(proposta_id, proposta)

@router.delete("/propostas/{proposta_id}")
async def delete_proposta(proposta_id: str):
    return await database.delete_proposta(proposta_id)
