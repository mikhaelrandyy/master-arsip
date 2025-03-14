from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from models.worker_role_model import WorkerRole

if  TYPE_CHECKING:
    from models import Role, Department

class WorkerBase(SQLModel):
    client_id: str = Field(nullable=True)
    status: bool = Field(default=True, nullable=False)
    department_id: str = Field(nullable=False, foreign_key='department.id')

class WorkerFullBase(BaseULIDModel, WorkerBase):
    pass

class Worker(WorkerFullBase, table=True):
    roles: list["Role"] = Relationship(link_model=WorkerRole, sa_relationship_kwargs={"lazy": "select"})
    department: "Department" = Relationship(sa_relationship_kwargs={"lazy": "select"})

    @property
    def department_name(self)-> str | None:
        return getattr(getattr(self, 'department', None), 'name', None)





    