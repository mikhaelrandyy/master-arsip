from models.base_model import SQLModel
from sqlmodel import Field, Relationship
from common.enum import JenisArsipEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocFormat


class DocTypeArchiveBase(SQLModel):
    doc_format_id: str | None = Field(nullable=False, foreign_key='doc_format.id', primary_key=True)
    doc_type_id: str | None = Field(nullable=False, foreign_key='doc_type.id', primary_key=True, default=None)
    jenis_arsip: JenisArsipEnum = Field(nullable=True)

class DocTypeArchive(DocTypeArchiveBase, table=True):
    doc_formats: list["DocFormat"] = Relationship(back_populates="doc_format_link", sa_relationship_kwargs = {"lazy": "select"})
    