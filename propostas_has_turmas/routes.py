from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import PropostaHasTurmas, PropostaHasTurmasInDB

router = APIRouter()

@router.get("/propostas_turmas/")
async def list_propostas_has_turmas():
    return await database.list_propostas_has_turmas()

@router.get("/propostas_turmas/{propostas_has_turmas_id}")
async def get_proposta_has_turmas(propostas_has_turmas_id: int):
    turma = await database.get_proposta_has_turmas(propostas_has_turmas_id)
    if turma:
        return turma
    else:
        raise HTTPException(status_code=404, detail="PropostaHasTurmas not found")

@router.post("/propostas_turmas/")
async def create_proposta_has_turmas(proposta_has_turmas: PropostaHasTurmas = Body(...)):
    new_proposta_has_turmas = await database.create_proposta_has_turmas(proposta_has_turmas)
    return new_proposta_has_turmas

@router.put("/propostas_turmas/{propostas_has_turmas_id}")
async def update_proposta_has_turmas(propostas_has_turmas_id: int, propostas_has_turmas: PropostaHasTurmas = Body(...)):
    return await database.update_proposta_has_turmas(propostas_has_turmas_id, propostas_has_turmas)

@router.delete("/propostas_turmas/{propostas_has_turmas_id}")
async def delete_proposta_has_turmas(propostas_has_turmas_id: int):
    return await database.delete_proposta_has_turmas(propostas_has_turmas_id)
