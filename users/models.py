from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: str
    cidades: List[str]

class UserInDB(User):
    _id: Optional[str] = None
    
