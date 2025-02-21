from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import JenisArsipEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.mapping_doc_format import DocumentFormat, MappingDocFormat

class JenisArsipBase(SQLModel):
    code: str | None = Field(nullable=True)
    name: JenisArsipEnum | None = Field(nullable=True)

class JenisArsipFullBase(BaseULIDModel, JenisArsipBase):
    pass

class JenisArsip(JenisArsipFullBase, table=True):
    doc_formats: list["DocumentFormat"] = Relationship(back_populates="jenis_arsips", link_model=MappingDocFormat, sa_relationship_kwargs = {"lazy": "select"})
