from pydantic import BaseModel
from typing import Optional

class Turma(BaseModel):
    name: str
    city: str
    state: str
    school: str

class TurmaInDB(Turma):
    _id: Optional[str] = None
    
