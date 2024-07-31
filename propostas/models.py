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
    genero_id: int
    user_id: int

class PropostaInDB(Proposta):
    _id: Optional[str] = None
    genero_id: Optional[int] = None
    user_id: Optional[int] = None

class GeneroResponse(BaseModel):
    id: int
    nome: str

class PropostaResponse(BaseModel):
    id: int
    tema: str
    min_palavras: int
    max_palavras: int
    data_aplicacao: datetime
    data_entrega: datetime
    dificuldade: str
    genero: GeneroResponse
