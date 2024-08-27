from pydantic import BaseModel
from typing import Optional, List

class Correcao(BaseModel):
    redacao_id: int
    nota: int

class CorrecaoInDB(Correcao):
    correcao_id: Optional[int] = None
    redacao_id: Optional[int] = None
 