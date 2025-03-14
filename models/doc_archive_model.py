from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from models.doc_archive_column_model import DocArchiveColumn
from typing import TYPE_CHECKING
from common.enum import PhysicalDocTypeEnum, JenisArsipEnum, StatusDocArchiveEnum


if TYPE_CHECKING:
    from models import DocType

class DocArchiveBase(SQLModel):
    doc_type_id: str | None = Field(nullable=True, foreign_key='doc_type.id')
    doc_format_id: str | None = Field(nullable=True, foreign_key='doc_format.id')
    doc_no: str | None = Field(nullable=True)
    doc_name: str | None = Field(nullable=True)
    doc_archive_ref_id: str | None = Field(nullable=True)
    unit_id: str | None = Field(nullable=True, foreign_key='unit.id')
    company_id: str | None  =  Field(nullable=True, foreign_key='company.id')
    alashak_id: str | None = Field(nullable=True, foreign_key='alashak.id')
    vendor_id: str | None = Field(nullable=True)
    project_id: str | None = Field(nullable=True, foreign_key='project.id')
    physical_doc_type: PhysicalDocTypeEnum = Field(nullable=False)
    remarks: str | None = Field(nullable=True)
    jenis_arsip: JenisArsipEnum = Field(nullable=False)
    status: StatusDocArchiveEnum | None = Field(nullable=True)
    
class DocArchiveFullBase(BaseULIDModel, DocArchiveBase):
    pass

class DocArchive(DocArchiveFullBase, table=True):
    doc_type: "DocType" = Relationship(sa_relationship_kwargs={"lazy": "select"})

    
    