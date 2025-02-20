from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import JenisArsipEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocumentFormat

class JenisArsipBase(SQLModel):
    code: str | None = Field(nullable=True)
    name: JenisArsipEnum | None = Field(nullable=True)
    doc_format_id: str | None = Field(nullable=True, foreign_key="document_format.id")

class JenisArsipFullBase(BaseULIDModel, JenisArsipBase):
    pass

class JenisArsip(JenisArsipFullBase, table=True):
    doc_formats: list["DocumentFormat"] = Relationship(back_populates="jenis_arsip", sa_relationship_kwargs = {"lazy": "select"})
    