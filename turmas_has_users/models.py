from pydantic import BaseModel
from typing import Optional, List

class TurmaHasUsers(BaseModel):
    user_id: int
    turma_id: int

class TurmaHasUsersInDB(TurmaHasUsers):
    _id: Optional[str] = None

    
