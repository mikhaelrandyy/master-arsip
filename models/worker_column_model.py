from sqlmodel import Field
from models.base_model import SQLModel

class WorkerColumnBase(SQLModel):
    worker_id: str = Field(nullable=True, foreign_key='worker.id', primary_key=True)
    role_id: str = Field(nullable=True, foreign_key='role.id', primary_key=True)
    project_id: str = Field(nullable=True, foreign_key='project.id', primary_key=True)
    departement_id: str = Field(nullable=True, foreign_key='departement.id', primary_key=True)
    
class WorkerColumn(WorkerColumnBase, table=True):
    pass