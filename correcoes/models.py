from pydantic import BaseModel
from typing import Optional, List

class Correcao(BaseModel):
    redacao_id: int
    comentarios: str
    nota: int

class CorrecaoInDB(Correcao):
    _id: Optional[str] = None
 