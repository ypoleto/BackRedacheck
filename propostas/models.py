from pydantic import BaseModel
from typing import Optional, List

class Proposta(BaseModel):
    tema: str
    genero: str
    min: str
    max: str
    aplicacao: str
    entrega: str
    dificuldade: str
    turmas: List[str]
    professor: str
    

class PropostaInDB(Proposta):
    _id: Optional[str] = None
    
