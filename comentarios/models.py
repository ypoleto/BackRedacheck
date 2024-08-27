from pydantic import BaseModel
from typing import Optional

class Comentario(BaseModel):
    comentario: str
    paragrafo_id: str
    correcao_id: int

class ComentarioInDB(Comentario):
    comentario_id: Optional[int] = None
 