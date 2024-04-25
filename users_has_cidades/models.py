from pydantic import BaseModel
from typing import Optional, List

class UsersHasCidades(BaseModel):
    user_id: int
    cidade: int

class UsersHasCidadesInDB(UsersHasCidades):
    _id: Optional[str] = None

    
