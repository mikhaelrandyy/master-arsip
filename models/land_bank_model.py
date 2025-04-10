from sqlmodel import SQLModel, Field
from models.base_model import BaseULIDModel
from decimal import Decimal

class LandBankBase(SQLModel):
    land_id: str | None = Field(nullable=True)
    project_id: str | None = Field(nullable=True, foreign_key='project.id')
    company_id: str | None = Field(nullable=True, foreign_key='company.id')
    desa_id: str | None = Field(nullable=True, foreign_key='desa.id')
    no_doc: str | None = Field(nullable=True)
    luas: Decimal | None = Field(nullable=True)
    luas_pemisahan: Decimal | None = Field(nullable=True)
    luas_sisa: Decimal | None = Field(nullable=True)

class LandBankFullBase(LandBankBase, BaseULIDModel):
    pass

class LandBank(LandBankFullBase, table=True):
    pass