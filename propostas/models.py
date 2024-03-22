from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Proposta(BaseModel):
    tema: str
    genero: str
    min: int
    max: int
    aplicacao: datetime
    entrega: datetime
    dificuldade: int
    turmas: List[str]
    professor: str
    

class PropostaInDB(Proposta):
    _id: Optional[str] = None
    
