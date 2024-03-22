from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import Genero, GeneroInDB

router = APIRouter()

@router.get("/generos/")
async def list_generos():
    return await database.list_generos()

@router.get("/generos/{genero_id}")
async def get_genero(genero_id: str):
    genero = await database.get_genero(genero_id)
    if genero:
        return genero
    else:
        raise HTTPException(status_code=404, detail="Genero não encontrada")

@router.post("/generos/")
async def create_genero(genero: Genero = Body(...)):
    new_genero = await database.create_genero(genero)
    return new_genero

@router.put("/generos/{genero_id}")
async def update_genero(genero_id: str, genero: Genero = Body(...)):
    return await database.update_genero(genero_id, genero)

@router.delete("/generos/{genero_id}")
async def delete_genero(genero_id: str):
    return await database.delete_genero(genero_id)
