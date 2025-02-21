from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocumentTypeGroup, DocumentFormat, Alashak, MappingDocType

class DocumentTypeBase(SQLModel):
    code: str | None = Field(nullable=True)
    name: str | None = Field(nullable=True)
    status: bool = Field(nullable=True)
    is_doc_asal: bool = Field(nullable=True)
    is_unit: bool = Field(nullable=True)
    alashak_id: str | None = Field(nullable=True, foreign_key="alashak.id")
    doc_type_group_id: str | None = Field(nullable=True, foreign_key="document_type_group.id")
    doc_format_id: str | None = Field(nullable=True, foreign_key="document_format.id")

class DocumentTypeFullBase(BaseULIDModel, DocumentTypeBase):
    pass

class DocumentType(DocumentTypeFullBase, table=True):
    alashak: "Alashak" = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    doc_type_group: "DocumentTypeGroup" = Relationship(back_populates="doc_types", sa_relationship_kwargs = {"lazy": "select"})
    doc_formats: list["DocumentFormat"] = Relationship(back_populates="doc_type", sa_relationship_kwargs = {"lazy": "select"})
    mapping_doc_types: list["MappingDocType"] = Relationship(back_populates="doc_type", sa_relationship_kwargs={"lazy": "select"})