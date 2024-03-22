from pymongo import MongoClient
from bson import ObjectId
from .models import CorrecaoInDB, Correcao
from typing import List

client = MongoClient('mongodb+srv://root:root@projeto.hufetlu.mongodb.net/?retryWrites=true&w=majority&appName=projeto')
db = client["test"]
collection = db["correcoes"]

async def create_correcao(correcao: Correcao) -> CorrecaoInDB:
    new_correcao = correcao.dict()
    result = collection.insert_one(new_correcao)
    new_correcao["_id"] = str(result.inserted_id)
    return CorrecaoInDB(**new_correcao)

async def list_correcoes() -> List[dict]:
    correcoes = []
    for correcao in collection.find():
        correcao["_id"] = str(correcao["_id"])
        correcoes.append(correcao)
    return correcoes

async def get_correcao(correcao_id: str) -> CorrecaoInDB:
    correcao = collection.find_one({"_id": ObjectId(correcao_id)})
    if correcao:
        correcao["_id"] = str(correcao["_id"])
        return CorrecaoInDB(**correcao)

async def update_correcao(correcao_id: str, correcao: Correcao) -> dict:
    result = collection.update_one({"_id": ObjectId(correcao_id)}, {"$set": correcao.dict()})
    if result.modified_count == 1:
        return {"message": "Correcao atualizada com sucesso"}

async def delete_correcao(correcao_id: str) -> dict:
    result = collection.delete_one({"_id": ObjectId(correcao_id)})
    if result.deleted_count == 1:
        return {"message": "Correcao deletada com sucesso"}
