from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import TypeDocFisikEnum
from typing import TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from models import Unit, Company, MemoDocAttachment

class MemoDocBase(SQLModel):
    doc_type_id: str | None = Field(nullable=True)
    unit_id: str | None = Field(foreign_key='unit.id')
    doc_no: str | None = Field(nullable=True)
    doc_name: str | None = Field(nullable=True)
    memo_id: str | None = Field(foreign_key='memo.id')
    alashak_id: str | None = Field(nullable=True)
    physical_doc_type: TypeDocFisikEnum = Field(nullable=True)
    remarks: str | None = Field(nullable=True)
    notaris_id: str | None = Field(nullable=True)
    doc_archive_id: str | None = Field(foreign_key='doc_archive.id')

class MemoDocFullBase(BaseULIDModel, MemoDocBase):
    pass

class MemoDoc(MemoDocFullBase, table=True):
    memo_doc_attachments: list["MemoDocAttachment"] = Relationship(sa_relationship_kwargs = {"lazy": "select"})



    
    