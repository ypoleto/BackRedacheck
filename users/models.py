from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    user_id: Optional[int] = None
    nome: str
    email: str
    password: Optional[str] = None
    tipo: str
    username: str

class UserInDB(User):
    _user_id: Optional[str] = None
    
