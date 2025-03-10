from models.base_model import BaseULIDModel, SQLModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocType

class DocTypeColumnBase(SQLModel):
    doc_type_id: str = Field(nullable=False, foreign_key='doc_type.id', primary_key=True)
    column_type_id: str = Field(nullable=False, foreign_key='column_type.id', primary_key=True)
    
class DocTypeColumn(DocTypeColumnBase, table=True):
    doc_type: "DocType" = Relationship(sa_relationship_kwargs = {"lazy": "select"})