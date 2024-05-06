from pydantic import BaseModel
from typing import Optional, List

class Turma(BaseModel):
    nome: str
    professor: int

class TurmaInDB(Turma):
    _id: Optional[str] = None
    
