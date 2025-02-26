from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field
from common.enum import JenisArsipEnum


class DocFormatJenisArsipDocTypeLinkBase(SQLModel):
    doc_format_id: str = Field(nullable=True, foreign_key='document_format.id', primary_key=True)
    doc_type_id: str = Field(nullable=True, foreign_key='document_type.id', primary_key=True)
    jenis_arsip: JenisArsipEnum = Field(nullable=True)

class DocFormatJenisArsipDocTypeLinkFullBase(BaseULIDModel, DocFormatJenisArsipDocTypeLinkBase):
    pass

class DocFormatJenisArsipDocTypeLink(DocFormatJenisArsipDocTypeLinkFullBase, table=True):
    pass