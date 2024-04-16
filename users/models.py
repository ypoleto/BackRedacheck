from pydantic import BaseModel
from typing import Optional, List
from turmas.models import TurmaInDB

class User(BaseModel):
    nome: str
    username: str
    email: str
    password: str
    tipo: str
    turmas: List[str]
    cidades: List[int]
    turma: Optional[str] 

class UserInDB(User):
    _id: Optional[str] = None
    
