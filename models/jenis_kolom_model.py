from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import TipeDataEnum
from typing import TYPE_CHECKING
from models.doc_type_jenis_kolom_model import DocTypeJenisKolomLink
from models.doc_arsip_kolom_model import DocArsipKolomLink


if TYPE_CHECKING:
    from models import DocumentType, DocumentArsip

class JenisKolomBase(SQLModel):
    name: str | None = Field(nullable=True)
    tipe_data: TipeDataEnum | None = Field(nullable=True)
    enum_data: str | None = Field(nullable=True)
    is_mandatory: bool = Field(nullable=True)
    is_show: bool = Field(nullable=True)
    
class JenisKolomFullBase(BaseULIDModel, JenisKolomBase):
    pass

class JenisKolom(JenisKolomFullBase, table=True):
    doc_types: list["DocumentType"] = Relationship(back_populates="jenis_koloms", link_model=DocTypeJenisKolomLink, sa_relationship_kwargs={"lazy": "select"})
    doc_arsips: list["DocumentArsip"] = Relationship(back_populates="jenis_koloms", link_model=DocArsipKolomLink, sa_relationship_kwargs={"lazy": "select"})

    