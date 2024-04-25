from pydantic import BaseModel
from typing import Optional, List

class Redacao(BaseModel):
    proposta: str
    aluno: str
    texto: str

class RedacaoInDB(Redacao):
    _id: Optional[str] = None
    
