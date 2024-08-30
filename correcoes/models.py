from pydantic import BaseModel
from typing import Optional, List

class Comentario(BaseModel):
    comentario: str
    paragrafo_id: str
    
class Correcao(BaseModel):
    redacao_id: int
    nota: int
    comentarios: Optional[List[Comentario]] = None

class CorrecaoInDB(Correcao):
    correcao_id: Optional[int] = None
    redacao_id: Optional[int] = None
 