from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import DocumentClassificationEnum
from typing import TYPE_CHECKING
from models.doc_format_jenis_arsip_doc_type_model import DocformatJenisarsipDoctype

if TYPE_CHECKING:
    from models import DocumentType

class DocumentFormatBase(SQLModel):
    code: str | None = Field(nullable=True, unique=True)
    name: str | None = Field(nullable=True)
    classification: DocumentClassificationEnum | None = Field(nullable=True)

class DocumentFormatFullBase(BaseULIDModel, DocumentFormatBase):
    pass

class DocumentFormat(DocumentFormatFullBase, table=True):
    doc_format_link: "DocformatJenisarsipDoctype" = Relationship(sa_relationship_kwargs = {"lazy": "select"})

    @property
    def jenis_arsip(self) -> str | None:
        return getattr(getattr(self, "doc_format_link", None), "jenis_arsip", None)