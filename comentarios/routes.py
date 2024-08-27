from fastapi import APIRouter, HTTPException, Body
from . import database
from .models import Comentario, ComentarioInDB

router = APIRouter()

@router.get("/comentarios/")
async def list_comentarios():
    return await database.list_comentarios()

@router.get("/comentarios/{comentario_id}")
async def get_comentario(comentario_id: int):
    comentario = await database.get_comentario(comentario_id)
    if comentario:
        return comentario
    else:
        raise HTTPException(status_code=404, detail="Comentario não encontrado")

@router.post("/comentarios/")
async def create_comentario(comentario: Comentario = Body(...)):
    new_comentario = await database.create_comentario(comentario)
    return new_comentario

@router.put("/comentarios/{comentario_id}")
async def update_comentario(comentario_id: int, comentario: Comentario = Body(...)):
    return await database.update_comentario(comentario_id, comentario)

@router.delete("/comentarios/{comentario_id}")
async def delete_comentario(comentario_id: int):
    return await database.delete_comentario(comentario_id)
