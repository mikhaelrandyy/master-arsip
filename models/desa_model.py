from sqlmodel import SQLModel, Field
from models.base_model import BaseULIDModel
from pydantic import field_validator

class DesaBase(SQLModel):
    code: str = Field(nullable=True, unique=True)
    name: str = Field(nullable=True, unique=True)

    @field_validator('code')
    def validate_code(cls, value):
        return value.upper()
    
    @field_validator('name')
    def validate_name(cls, value):
        return value.strip()

class DesaFullBase(DesaBase, BaseULIDModel):
    pass

class Desa(DesaFullBase, table=True):
    pass