from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import DocumentClassificationEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.mapping_doc_format import MappingDocFormat
    from models import JenisArsip

class DocumentFormatBase(SQLModel):
    code: str | None = Field(nullable=True)
    name: str | None = Field(nullable=True)
    classification: DocumentClassificationEnum | None = Field(nullable=True)

class DocumentFormatFullBase(BaseULIDModel, DocumentFormatBase):
    pass

class DocumentFormat(DocumentFormatFullBase, table=True):
    jenis_arsips: list["JenisArsip"] = Relationship(back_populates="doc_formats", link_model=MappingDocFormat, sa_relationship_kwargs = {"lazy": "select"})

    