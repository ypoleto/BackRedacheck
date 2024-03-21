from pymongo import MongoClient
from bson import ObjectId
from .models import TurmaInDB, Turma
from typing import List

client = MongoClient('mongodb+srv://root:root@projeto.hufetlu.mongodb.net/?retryWrites=true&w=majority&appName=projeto')
db = client["test"]
collection = db["turmas"]

async def create_turma(turma: Turma) -> TurmaInDB:
    new_turma = turma.dict()
    result = collection.insert_one(new_turma)
    new_turma["_id"] = str(result.inserted_id)
    return TurmaInDB(**new_turma)

async def list_turmas() -> List[dict]:
    turmas = []
    for turma in collection.find():
        turma["_id"] = str(turma["_id"])
        turmas.append(turma)
    return turmas

async def get_turma(turma_id: str) -> TurmaInDB:
    turma = collection.find_one({"_id": ObjectId(turma_id)})
    if turma:
        turma["_id"] = str(turma["_id"])
        return TurmaInDB(**turma)

async def update_turma(turma_id: str, turma: Turma) -> dict:
    result = collection.update_one({"_id": ObjectId(turma_id)}, {"$set": turma.dict()})
    if result.modified_count == 1:
        return {"message": "Turma atualizada com sucesso"}

async def delete_turma(turma_id: str) -> dict:
    result = collection.delete_one({"_id": ObjectId(turma_id)})
    if result.deleted_count == 1:
        return {"message": "Turma deletada com sucesso"}
