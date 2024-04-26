from pydantic import BaseModel
from typing import Optional, List

class PropostaHasTurmas(BaseModel):
    proposta_id: int
    turma_id: int

class PropostaHasTurmasInDB(PropostaHasTurmas):
    _id: Optional[str] = None

    
