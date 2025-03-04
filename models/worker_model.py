# from models.base_model import BaseULIDModel
# from sqlmodel import SQLModel, Field, Relationship
# from typing import TYPE_CHECKING
# from models.worker_role_model import WorkerRoleLink

# if  TYPE_CHECKING:
#     from models import Role

# class WorkerBase(SQLModel):
#     user_id: str = Field(nullable=True)
#     departement_id: str = Field(nullable=True, foreign_key='departement.id')
#     status: bool = Field(default=True)

# class WorkerFullBase(BaseULIDModel, WorkerBase):
#     pass

# class Worker(WorkerFullBase, table=True):
#     roles: list["Role"] = Relationship(link_model=WorkerRoleLink, sa_relationship_kwargs={"lazy": "select"})
    