from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    password: str
    user_type: str

class UserInDB(User):
    _id: Optional[str] = None
    
