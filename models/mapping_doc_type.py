from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocumentType

class MappingDocTypeBase(SQLModel):
    doc_type_id: str | None = Field(nullable=True, foreign_key='document_type.id')

class MappingDocTypeFullBase(BaseULIDModel, MappingDocTypeBase):
    pass

class MappingDocType(MappingDocTypeFullBase, table=True):
    doc_type: "DocumentType" = Relationship(back_populates="mapping_doc_types", sa_relationship_kwargs = {"lazy": "select"})
    