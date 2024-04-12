from pymongo import MongoClient
from bson import ObjectId
from .models import UserInDB, User
from passlib.context import CryptContext
from turmas.database import get_turma
from typing import List

client = MongoClient('mongodb+srv://root:root@projeto.hufetlu.mongodb.net/?retryWrites=true&w=majority&appName=projeto')
db = client["test"]
collection = db["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


async def create_user(user: User) -> UserInDB:
    new_user = user.dict()
    new_user["hashed_password"] = get_password_hash(new_user["password"])
    result = collection.insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)
    print('new_user', new_user)
    return UserInDB(**new_user)

async def list_users() -> List[dict]:
    users = []
    for user in collection.find():
        user.pop("password", None)
        user.pop("hashed_password", None)
        user["_id"] = str(user["_id"])
        
        
        users.append(user)
    return users

async def get_user(user_id: str) -> UserInDB:
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user.pop("hashed_password", None)
        user.pop("password", None)
        user["_id"] = str(user["_id"])
        
        turma_id = user["turmas"][0]
        turma = await get_turma(turma_id)
        print(turma)
        user["turma"] = turma  
        
        user.setdefault("password", "")
        return UserInDB(**user)

async def update_user(user_id: str, user: User) -> dict:
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
    if result.modified_count == 1:
        return {"message": "User updated successfully"}

async def delete_user(user_id: str) -> dict:
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
