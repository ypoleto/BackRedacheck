
from typing import List, Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None # type: ignore

class User(BaseModel):
    username: str
    email: Optional[str] = None
    nome: Optional[str] = None
    disabled: Optional[bool] = None
    tipo: Optional[str]
    turmas: Optional[List[str]]
    cidades: Optional[List[int]]

class UserInDB(User):
    hashed_password: str