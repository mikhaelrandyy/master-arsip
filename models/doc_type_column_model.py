from models.base_model import BaseULIDModel, SQLModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocType

class DocTypeColumnBase(SQLModel):
    doc_type_id: str = Field(nullable=False, foreign_key='document_type.id', primary_key=True)
    jenis_kolom_id: str = Field(nullable=False, foreign_key='jenis_kolom.id', primary_key=True)
    
class DocTypeColumn(DocTypeColumnBase, table=True):
    document_type: "DocType" = Relationship(sa_relationship_kwargs = {"lazy": "select"})