from pydantic import BaseModel
from typing import Optional, List

class Turma(BaseModel):
    nome: str
    professor: int
    colegio: str
    turma_ativa: int

class TurmaInDB(Turma):
    _id: Optional[str] = None
    
