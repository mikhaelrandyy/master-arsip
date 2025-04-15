from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field
from pydantic import field_validator

class AlashakBase(SQLModel):
    code: str | None = Field(default=None, nullable=False, unique=True)
    name: str = Field(nullable=False)

    @field_validator('code')
    def validate_code(cls, value):
        return value.upper()
    
    @field_validator('name')
    def validate_name(cls, value):
        return value.strip()

class AlashakFullBase(BaseULIDModel, AlashakBase):
    pass

class Alashak(AlashakFullBase, table=True):
    pass