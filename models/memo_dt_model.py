from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import TypeDocFisikEnum
from typing import TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from models import Unit, Company, MemoAttachment

class MemoDtBase(SQLModel):
    doc_type_id: str | None = Field(nullable=True)
    unit_id: str | None = Field(foreign_key='unit.id')
    nomor: str | None = Field(nullable=True)
    name: str | None = Field(nullable=True)
    company_id: str | None = Field(foreign_key='company.id')
    tanggal: date = Field(nullable=True)
    alashak_id: str | None = Field(nullable=True)
    tipe_doc_fisik: TypeDocFisikEnum = Field(nullable=True)
    remarks: str | None = Field(nullable=True)

class MemoDtFullBase(BaseULIDModel, MemoDtBase):
    pass

class MemoDt(MemoDtFullBase, table=True):
    attachments: list["MemoAttachment"] = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    unit: list["Unit"] = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    companys: list["Company"] = Relationship(sa_relationship_kwargs = {"lazy": "select"})



    
    