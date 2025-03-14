from models.base_model import BaseULIDModel, SQLModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Department

class DepartmentDocTypeBase(SQLModel):
    doc_type_id: str = Field(nullable=False, foreign_key='doc_type.id', primary_key=True)
    department_id: str = Field(nullable=False, foreign_key='department.id', primary_key=True)
    
class DepartmentDocType(DepartmentDocTypeBase, table=True):
    pass