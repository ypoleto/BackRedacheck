
from typing import List, Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username:str

class User(BaseModel):
    user_id: int
    username: str
    email: str
    nome: Optional[str] = None
    tipo: str
    turmas: List[str] = []
    cidades: List[str] = []
    
    
class UserInDB(User):
    hashed_password: Optional[str]