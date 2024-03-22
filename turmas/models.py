from pydantic import BaseModel
from typing import Optional, List

class Turma(BaseModel):
    nome: str
    cidade: str
    estado: str
    escola: str
    professor: str
    alunos: List[str]
    

class TurmaInDB(Turma):
    _id: Optional[str] = None
    
