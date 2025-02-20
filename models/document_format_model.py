from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import DocumentClassificationEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocumentType, JenisArsip

class DocumentFormatBase(SQLModel):
    code: str | None = Field(nullable=True)
    name: str | None = Field(nullable=True)
    classification: DocumentClassificationEnum | None = Field(nullable=True)

class DocumentFormatFullBase(BaseULIDModel, DocumentFormatBase):
    pass

class DocumentFormat(DocumentFormatFullBase, table=True):
    doc_type: "DocumentType" = Relationship(back_populates="doc_formats", sa_relationship_kwargs = {"lazy": "select"})
    jenis_arsip: "JenisArsip" = Relationship(back_populates="doc_formats", sa_relationship_kwargs = {"lazy": "select"})

    