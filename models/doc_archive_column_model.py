from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocArchive, ColumnType


class DocArchiveColumnBase(SQLModel):
    doc_archive_id: str | None = Field(nullable=True, foreign_key='doc_archive.id')
    column_type_id: str | None = Field(nullable=True, foreign_key='column_type.id')
    value: str | None = Field(nullable=True)

class DocArchiveColumnFullBase(BaseULIDModel, DocArchiveColumnBase):
    pass

class DocArchiveColumn(DocArchiveColumnFullBase, table=True):
    doc_archives: list["DocArchive"] = Relationship(sa_relationship_kwargs={"lazy": "select"})
    column_types: list["ColumnType"] = Relationship(sa_relationship_kwargs={"lazy": "select"})

    