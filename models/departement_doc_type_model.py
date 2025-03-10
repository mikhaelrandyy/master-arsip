from models.base_model import BaseULIDModel, SQLModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Departement

class DepartementDocTypeBase(SQLModel):
    doc_type_id: str = Field(nullable=False, foreign_key='doc_type.id', primary_key=True)
    dept_id: str = Field(nullable=False, foreign_key='departement.id', primary_key=True)
    
class DepartementDocType(DepartementDocTypeBase, table=True):
    pass