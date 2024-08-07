from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    nome: str
    email: str
    password: Optional[str] = None
    tipo: str
    username: str
    turma: Optional[str] = None

class UserInDB(User):
    _user_id: Optional[str] = None
    
