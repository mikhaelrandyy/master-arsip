from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import DocumentCategoryEnum, NecessityEnum, JenisArsipEnum, OutgoingToTypeEnum, OutgoingToDocTypeEnum
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocFormat, Company, Project

class MemoBase(SQLModel):
    code: str | None = Field(nullable=True, unique=True)
    jenis_arsip: JenisArsipEnum = Field(nullable=False)
    doc_category: DocumentCategoryEnum = Field(nullable=False)
    doc_format_id: str | None = Field(foreign_key='doc_format.id')
    project_id: str = Field(nullable=False, foreign_key='project.id')
    company_id: str = Field(nullable=False, foreign_key='company.id')
    necessity: NecessityEnum | None = Field(nullable=True)
    file_name: str | None = Field(nullable=True)
    file_url: str | None = Field(nullable=True)
    return_date: date | None = Field(nullable=True)
    remarks:str | None = Field(nullable=True)
    outgoing_to_type: OutgoingToTypeEnum | None = Field(nullable=True)
    outgoing_to_notaris_id: str | None = Field(nullable=True)
    outgoing_to_department_id: str | None = Field(nullable=True, foreign_key="department.id")
    outgoing_doc_type: OutgoingToDocTypeEnum | None = Field(nullable=True)
    outgoing_to_jenis_arsip: JenisArsipEnum | None = Field(nullable=True)
    workflow_id: str | None = Field(foreign_key="workflow.id", nullable=True)

class MemoFullBase(BaseULIDModel, MemoBase):
    pass

class Memo(MemoFullBase, table=True):
    pass
    



    
    