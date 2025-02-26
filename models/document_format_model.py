from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import DocumentClassificationEnum
from typing import TYPE_CHECKING
from models.doc_format_jenis_arsip_doc_type_model import DocFormatJenisArsipDocTypeLink

if TYPE_CHECKING:
    from models import DocumentType

class DocumentFormatBase(SQLModel):
    code: str | None = Field(nullable=True)
    name: str | None = Field(nullable=True)
    classification: DocumentClassificationEnum | None = Field(nullable=True)

class DocumentFormatFullBase(BaseULIDModel, DocumentFormatBase):
    pass

class DocumentFormat(DocumentFormatFullBase, table=True):
    doc_types: list["DocumentType"] = Relationship(back_populates="doc_formats", link_model=DocFormatJenisArsipDocTypeLink, sa_relationship_kwargs = {"lazy": "select"})

    