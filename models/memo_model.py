from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import DocumentCategoryEnum, NecessityEnum, JenisArsipEnum, OutgoingtoTypeEnum, OutgoingToDocType
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocFormat, Company, Project

class MemoBase(SQLModel):
    code: str | None = Field(nullable=True, unique=True)
    jenis_arsip: JenisArsipEnum = Field(nullable=True)
    doc_category: DocumentCategoryEnum = Field(nullable=True)
    doc_format_id: str | None = Field(foreign_key='doc_format.id')
    project_id: str | None = Field(foreign_key='project.id')
    company_id: str | None = Field(foreign_key='company.id')
    necessity: NecessityEnum = Field(nullable=True)
    file_name: str | None = Field(nullable=True)
    file_url: str | None = Field(nullable=True)
    return_date: date | None = Field(nullable=True)
    remarks:str | None = Field(nullable=True)
    outgoing_to_type: OutgoingtoTypeEnum = Field(nullable=True)
    outgoing_to_notaris_id: str | None = Field(nullable=True)
    outgoing_to_departement_id: str | None = Field(nullable=True)
    outgoing_doc_type: OutgoingToDocType = Field(nullable=True)
    outgoing_to_jenis_arsip: JenisArsipEnum = Field(nullable=True)


class MemoFullBase(BaseULIDModel, MemoBase):
    pass

class Memo(MemoFullBase, table=True):
    project: "Project" = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    company: "Company" = Relationship(sa_relationship_kwargs = {"lazy": "select"})

    @property
    def project_code(self) -> str | None:
        return getattr(getattr(self, 'project', None), 'code', None)
    
    @property
    def company_code(self) -> str | None:
        return getattr(getattr(self, 'company', None), 'code', None)
    



    
    