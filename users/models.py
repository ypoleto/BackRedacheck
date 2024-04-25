from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    nome: str
    email: str
    password: Optional[str] = None
    tipo: str
    username: str
    turmas: Optional[str] = None
    cidades: Optional[str] = None

class UserInDB(User):
    _id: Optional[str] = None
    
