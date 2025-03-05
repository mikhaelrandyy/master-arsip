from models.base_model import BaseULIDModel
from pydantic import field_validator
from sqlmodel import SQLModel, Field

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
    