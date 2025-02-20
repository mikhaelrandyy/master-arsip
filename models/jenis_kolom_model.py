from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field
from common.enum import TipeDataEnum

class JenisKolomBase(SQLModel):
    name: str | None = Field(nullable=True)
    tipe_data: TipeDataEnum | None = Field(nullable=True)
    enum_data: str | None = Field(nullable=True)
    is_mandatory: bool = Field(nullable=True)
    is_show: bool = Field(nullable=True)
    
class JenisKolomFullBase(BaseULIDModel, JenisKolomBase):
    pass

class JenisKolom(JenisKolomFullBase, table=True):
    pass