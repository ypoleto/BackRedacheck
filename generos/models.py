from pydantic import BaseModel
from typing import Optional, List

class Genero(BaseModel):
    nome: str

class GeneroInDB(Genero):
    _id: Optional[str] = None
    
