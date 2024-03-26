from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    nome: str
    username: str
    email: str
    password: str
    tipo: str
    turma: str
    cidades: List[str]

class UserInDB(User):
    _id: Optional[str] = None
    
