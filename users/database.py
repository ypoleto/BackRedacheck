from pymongo import MongoClient
from bson import ObjectId
from .models import UserInDB, User
from typing import List

client = MongoClient('mongodb+srv://root:root@projeto.hufetlu.mongodb.net/?retryWrites=true&w=majority&appName=projeto')
db = client["test"]
collection = db["users"]

async def create_user(user: User) -> UserInDB:
    new_user = user.dict()
    result = collection.insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)
    return UserInDB(**new_user)

async def list_users() -> List[dict]:
    users = []
    for user in collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

async def get_user(user_id: str) -> UserInDB:
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return UserInDB(**user)

async def update_user(user_id: str, user: User) -> dict:
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
    if result.modified_count == 1:
        return {"message": "User updated successfully"}

async def delete_user(user_id: str) -> dict:
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
