from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from models.worker_role_model import WorkerRole

if  TYPE_CHECKING:
    from models import Worker

class RoleBase(SQLModel):
    name: str = Field(nullable=True)

class RoleFullBase(BaseULIDModel, RoleBase):
    pass

class Role(RoleFullBase, table=True):
    workers: list["Worker"] = Relationship(link_model=WorkerRole, sa_relationship_kwargs={"lazy": "select"})
    