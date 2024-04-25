from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Proposta(BaseModel):
    tema: str
    min_palavras: int
    max_palavras: int
    data_aplicacao: datetime
    data_entrega: datetime
    dificuldade: str
    genero: int
    professor: int
    

class PropostaInDB(Proposta):
    _id: Optional[str] = None
    
