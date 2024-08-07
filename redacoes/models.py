from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class Redacao(BaseModel):
    texto: str
    titulo: str
    proposta_id: int
    user_id: int
    data_envio: datetime
    status: int

class RedacaoInDB(Redacao):
    redacao_id: Optional[int] = None
    
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

class AlunoResponse(BaseModel):
    id: int
    nome: str

class RedacaoResponse(BaseModel):
    id: int
    texto: str
    titulo: str
    data_envio: datetime
    status: int
    proposta: PropostaResponse
    aluno: AlunoResponse