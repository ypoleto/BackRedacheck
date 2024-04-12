from pymongo import MongoClient
from bson import ObjectId
from .models import RedacaoInDB, Redacao
from typing import List
from propostas.database import get_proposta
from turmas.database import get_turma
from users.database import get_user

client = MongoClient('mongodb+srv://root:root@projeto.hufetlu.mongodb.net/?retryWrites=true&w=majority&appName=projeto')
db = client["test"]
collection = db["redacoes"]

async def create_redacao(redacao: Redacao) -> RedacaoInDB:
    new_redacao = redacao.dict()
    result = collection.insert_one(new_redacao)
    new_redacao["_id"] = str(result.inserted_id)
    return RedacaoInDB(**new_redacao)

async def list_redacoes() -> List[dict]:
    redacoes = []
    for redacao in collection.find():
        redacao["_id"] = str(redacao["_id"])
        
        aluno_id = redacao["aluno"]
        aluno = await get_user(aluno_id)
        redacao["aluno"] = aluno  
        
        proposta_id = redacao["proposta"]
        proposta = await get_proposta(proposta_id)
        redacao["proposta"] = proposta  
        
        redacoes.append(redacao)
    return redacoes

async def get_redacao(redacao_id: str) -> RedacaoInDB:
    redacao = collection.find_one({"_id": ObjectId(redacao_id)})
    if redacao:
        redacao["_id"] = str(redacao["_id"])
        return RedacaoInDB(**redacao)

async def update_redacao(redacao_id: str, redacao: Redacao) -> dict:
    result = collection.update_one({"_id": ObjectId(redacao_id)}, {"$set": redacao.dict()})
    if result.modified_count == 1:
        return {"message": "Redacao atualizada com sucesso"}

async def delete_redacao(redacao_id: str) -> dict:
    result = collection.delete_one({"_id": ObjectId(redacao_id)})
    if result.deleted_count == 1:
        return {"message": "Redacao deletada com sucesso"}
