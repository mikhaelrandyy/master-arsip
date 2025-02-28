from models.base_model import SQLModel
from sqlmodel import Field, Relationship
from common.enum import JenisArsipEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocumentFormat


class DocformatJenisarsipDoctypeBase(SQLModel):
    doc_format_id: str | None = Field(nullable=False, foreign_key='document_format.id', primary_key=True)
    doc_type_id: str | None = Field(nullable=False, foreign_key='document_type.id', primary_key=True)
    jenis_arsip: JenisArsipEnum | None = Field(nullable=False, primary_key=True)

class DocformatJenisarsipDoctype(DocformatJenisarsipDoctypeBase, table=True):
    doc_formats: list["DocumentFormat"] = Relationship(back_populates="doc_format_link", sa_relationship_kwargs = {"lazy": "select"})
    