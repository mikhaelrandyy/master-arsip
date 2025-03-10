from sqlmodel import Field
from models.base_model import SQLModel

class WorkerRoleBase(SQLModel):
    worker_id: str = Field(nullable=True, primary_key=True, foreign_key='worker.id')
    role_id: str = Field(nullable=True, primary_key=True, foreign_key='role.id')
    
class WorkerRole(WorkerRoleBase, table=True):
    pass    