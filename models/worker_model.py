from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from models.worker_role_model import WorkerRole

if  TYPE_CHECKING:
    from models import Role, Departement

class WorkerBase(SQLModel):
    client_id: str = Field(nullable=True)
    status: bool = Field(default=True)
    departement_id: str = Field(nullable=True, foreign_key='departement.id')

class WorkerFullBase(BaseULIDModel, WorkerBase):
    pass

class Worker(WorkerFullBase, table=True):
    roles: list["Role"] = Relationship(back_populates="workers", link_model=WorkerRole, sa_relationship_kwargs={"lazy": "select"})
    departement: "Departement" = Relationship(back_populates="worker", sa_relationship_kwargs={"lazy": "select"})

    @property
    def departement_name(self)-> str | None:
        return getattr(getattr(self, 'departement', None), 'name', None)





    