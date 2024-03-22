from pydantic import BaseModel
from typing import Optional, List

class Correcao(BaseModel):
    redacao: str
    comentarios: str
    nota: int

class CorrecaoInDB(Correcao):
    _id: Optional[str] = None
    
