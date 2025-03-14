from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import PhysicalDocTypeEnum
from typing import TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from models import Unit, Company, MemoDocAttachment

class MemoDocBase(SQLModel):
    memo_id: str | None = Field(nullable=False, foreign_key='memo.id')
    doc_archive_id: str | None = Field(foreign_key='doc_archive.id')
    doc_type_id: str = Field(nullable=False)
    doc_no: str = Field(nullable=False)
    doc_name: str | None = Field(nullable=True)
    unit_id: str | None = Field(foreign_key='unit.id')
    alashak_id: str | None = Field(nullable=True, foreign_key='alashak.id')
    physical_doc_type: PhysicalDocTypeEnum = Field(nullable=False)
    remarks: str | None = Field(nullable=True)
    vendor_id: str | None = Field(nullable=True)

class MemoDocFullBase(BaseULIDModel, MemoDocBase):
    pass

class MemoDoc(MemoDocFullBase, table=True):pass



    
    