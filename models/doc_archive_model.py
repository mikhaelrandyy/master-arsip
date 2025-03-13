from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from models.doc_archive_column_model import DocArchiveColumn
from typing import TYPE_CHECKING
from common.enum import TypeDocFisikEnum, JenisArsipEnum, StatusDocArchiveEnum


if TYPE_CHECKING:
    from models import DocType

class DocArchiveBase(SQLModel):
    doc_type_id: str | None = Field(nullable=True, foreign_key='doc_type.id')
    unit_id: str | None = Field(nullable=True, foreign_key='unit.id')
    company_id: str | None  =  Field(nullable=True, foreign_key='company.id')
    alashak_id: str | None = Field(nullable=True, foreign_key='alashak.id')
    notaris_id: str | None = Field(nullable=True)
    doc_format_id: str | None = Field(nullable=True, foreign_key='doc_format.id')
    project_id: str | None = Field(nullable=True, foreign_key='project.id')
    doc_no: str | None = Field(nullable=True)
    doc_name: str | None = Field(nullable=True)
    physical_doc_type: TypeDocFisikEnum = Field(nullable=True)
    remarks: str | None = Field(nullable=True)
    jenis_arsip: JenisArsipEnum = Field(nullable=True)
    status: StatusDocArchiveEnum = Field(nullable=True)
    
    

class DocArchiveFullBase(BaseULIDModel, DocArchiveBase):
    pass

class DocArchive(DocArchiveFullBase, table=True):
    doc_types: list["DocType"] = Relationship(sa_relationship_kwargs={"lazy": "select"})

    
    