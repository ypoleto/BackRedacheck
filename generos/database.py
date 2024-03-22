from pymongo import MongoClient
from bson import ObjectId
from .models import GeneroInDB, Genero
from typing import List

client = MongoClient("mongodb+srv://root:root@projeto.hufetlu.mongodb.net/?retryWrites=true&w=majority&appName=projeto")
db = client["test"]
collection = db["generos"]


async def create_genero(genero: Genero) -> GeneroInDB:
    new_genero = genero.dict()
    result = collection.insert_one(new_genero)
    new_genero["_id"] = str(result.inserted_id)
    return GeneroInDB(**new_genero)


async def list_generos() -> List[dict]:
    generos = []
    for genero in collection.find():
        genero["_id"] = str(genero["_id"])
        generos.append(genero)
    return generos


async def get_genero(genero_id: str) -> GeneroInDB:
    genero = collection.find_one({"_id": ObjectId(genero_id)})
    if genero:
        genero["_id"] = str(genero["_id"])
        return GeneroInDB(**genero)


async def update_genero(genero_id: str, genero: Genero) -> dict:
    result = collection.update_one(
        {"_id": ObjectId(genero_id)}, {"$set": genero.dict()}
    )
    if result.modified_count == 1:
        updated_genero = collection.find_one({"_id": ObjectId(genero_id)})
        return {
            "message": "Genero atualizado com sucesso",
            "result": GeneroInDB(**updated_genero),
        }


async def delete_genero(genero_id: str) -> dict:
    result = collection.delete_one({"_id": ObjectId(genero_id)})
    if result.deleted_count == 1:
        return {"message": "Genero deletado com sucesso"}
