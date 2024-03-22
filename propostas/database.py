from pymongo import MongoClient
from bson import ObjectId
from .models import PropostaInDB, Proposta
from typing import List

client = MongoClient('mongodb+srv://root:root@projeto.hufetlu.mongodb.net/?retryWrites=true&w=majority&appName=projeto')
db = client["test"]
collection = db["propostas"]

async def create_proposta(proposta: Proposta) -> PropostaInDB:
    new_proposta = proposta.dict()
    result = collection.insert_one(new_proposta)
    new_proposta["_id"] = str(result.inserted_id)
    return PropostaInDB(**new_proposta)

async def list_propostas() -> List[dict]:
    propostas = []
    for proposta in collection.find():
        proposta["_id"] = str(proposta["_id"])
        propostas.append(proposta)
    return propostas

async def get_proposta(proposta_id: str) -> PropostaInDB:
    proposta = collection.find_one({"_id": ObjectId(proposta_id)})
    if proposta:
        proposta["_id"] = str(proposta["_id"])
        return PropostaInDB(**proposta)

async def update_proposta(proposta_id: str, proposta: Proposta) -> dict:
    result = collection.update_one({"_id": ObjectId(proposta_id)}, {"$set": proposta.dict()})
    if result.modified_count == 1:
        return {"message": "Proposta atualizada com sucesso"}

async def delete_proposta(proposta_id: str) -> dict:
    result = collection.delete_one({"_id": ObjectId(proposta_id)})
    if result.deleted_count == 1:
        return {"message": "Proposta deletada com sucesso"}
