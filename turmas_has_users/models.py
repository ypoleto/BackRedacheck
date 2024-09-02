from pydantic import BaseModel
from typing import Optional, List

class UserResponse(BaseModel):
    user_id: int
    nome: str
    username: str
    
class TurmaHasUsers(BaseModel):
    turmas_users_id: Optional[int] = None
    turma_id: int
    user_id: int

class TurmaHasUsersResponse(BaseModel):
    turmas_has_users_id: Optional[int] = None
    turma_id: int
    user: UserResponse

class TurmaHasUsersInDB(TurmaHasUsers):
    _id: Optional[str] = None

    
