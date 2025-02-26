from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from models.doc_format_jenis_arsip_doc_type_model import DocFormatJenisArsipDocTypeLink
from models.doc_type_jenis_kolom_model import DocTypeJenisKolomLink

if TYPE_CHECKING:
    from models import DocumentTypeGroup, DocumentFormat, Alashak, JenisKolom

class DocumentTypeBase(SQLModel):
    code: str | None = Field(nullable=True)
    name: str | None = Field(nullable=True)
    status: bool = Field(nullable=True)
    is_doc_asal: bool = Field(nullable=True)
    is_unit: bool = Field(nullable=True)
    alashak_id: str | None = Field(nullable=True, foreign_key="alashak.id")
    doc_type_group_id: str | None = Field(nullable=True, foreign_key="document_type_group.id")

class DocumentTypeFullBase(BaseULIDModel, DocumentTypeBase):
    pass

class DocumentType(DocumentTypeFullBase, table=True):
    alashak: "Alashak" = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    doc_type_group: "DocumentTypeGroup" = Relationship(back_populates="doc_types", sa_relationship_kwargs = {"lazy": "select"})
    doc_formats: list["DocumentFormat"] = Relationship(back_populates="doc_types", link_model=DocFormatJenisArsipDocTypeLink, sa_relationship_kwargs = {"lazy": "select"})
    jenis_koloms: list["JenisKolom"] = Relationship(back_populates="doc_types", link_model=DocTypeJenisKolomLink, sa_relationship_kwargs={"lazy": "select"})