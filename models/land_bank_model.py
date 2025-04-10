from sqlmodel import Field
from models.base_model import BaseULIDModel, SQLModel
from decimal import Decimal

class LandBankBase(SQLModel):
    code: str | None = Field(nullable=False)
    descs: str | None = Field(nullable=True, default=None)
    project_id: str = Field(nullable=False, foreign_key='project.id')
    company_id: str = Field(nullable=False, foreign_key='company.id')
    desa_id: str = Field(nullable=False, foreign_key='desa.id')
    alashak_id: str | None = Field(nullable=True, foreign_key="alashak.id")
    doc_no: str = Field(nullable=False)
    reason: str | None = Field(nullable=True, default=None)
    luas_tanah: Decimal = Field(nullable=False, default=0)
    luas_awal: Decimal | None = Field(nullable=True, default=0)
    luas_sertifikat: Decimal | None = Field(nullable=True, default=0)
    parent_id: str | None = Field(nullable=True, foreign_key="land_bank.id")

class LandBankFullBase(LandBankBase, BaseULIDModel):
    pass

class LandBank(LandBankFullBase, table=True):
    pass