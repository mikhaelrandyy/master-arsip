from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from models.worker_column_model import WorkerColumn

if  TYPE_CHECKING:
    from models import Role

class WorkerBase(SQLModel):
    client_id: str = Field(nullable=True)
    status: bool = Field(default=True)

class WorkerFullBase(BaseULIDModel, WorkerBase):
    pass

class Worker(WorkerFullBase, table=True):
    roles: list["Role"] = Relationship(back_populates="workers", link_model=WorkerColumn, sa_relationship_kwargs={"lazy": "select"})


    