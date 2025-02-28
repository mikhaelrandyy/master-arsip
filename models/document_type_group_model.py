from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocumentType

class DocumentTypeGroupBase(SQLModel):
    code: str | None = Field(nullable=True)
    name: str | None = Field(nullable=True)

class DocumentTypeGroupFullBase(BaseULIDModel, DocumentTypeGroupBase):
    pass

class DocumentTypeGroup(DocumentTypeGroupFullBase, table=True):
    document_types: list["DocumentType"] = Relationship(back_populates="document_type_group", sa_relationship_kwargs = {"lazy": "select"})
