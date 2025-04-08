from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from models.department_doc_type_model import DepartmentDocType
from typing  import TYPE_CHECKING
from pydantic import field_validator

if TYPE_CHECKING:
    from models import DocType, Worker

class DepartmentBase(SQLModel):
    code: str | None = Field(nullable=False, default=None, unique=True)
    name: str | None = Field(nullable=False, unique=True)

    @field_validator('code')
    def validate_code(cls, value):
        return value.upper()
    
    @field_validator('name')
    def validate_name(cls, value):
        return value.upper()

class DepartmentFullBase(BaseULIDModel, DepartmentBase):pass

class Department(DepartmentFullBase, table=True):pass