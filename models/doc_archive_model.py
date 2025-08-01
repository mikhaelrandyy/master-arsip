from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field
from common.enum import PhysicalDocTypeEnum, JenisArsipEnum, StatusDocArchiveEnum


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
    is_transfer: bool | None = Field(nullable=True, default=False)
    safe_location: str | None = Field(nullable=True)
    land_bank_id: str | None = Field(nullable=True, foreign_key='land_bank.id')
    
class DocArchiveFullBase(BaseULIDModel, DocArchiveBase):
    pass

class DocArchive(DocArchiveFullBase, table=True):
    pass

    
    