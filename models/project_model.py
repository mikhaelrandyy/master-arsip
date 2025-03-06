from models.base_model import BaseULIDModel
from sqlmodel import Relationship
from pydantic import field_validator
from sqlmodel import SQLModel, Field
from models.worker_role_model import WorkerRole

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Worker

class ProjectBase(SQLModel):
    code: str = Field(nullable=False, max_length=4, unique=True)
    name: str = Field(nullable=False, max_length=100)
    area_id:str | None = Field(nullable=True)

    @field_validator('code')
    def validate_code(cls, value):
        return value.upper()

class ProjectFullBase(BaseULIDModel, ProjectBase):
    pass

class Project(ProjectFullBase, table=True):
    pass
    