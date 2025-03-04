from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from models.doc_archive_kolom_model import DocArchiveKolomLink
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import ColumnType

class DocArchiveBase(SQLModel):
    doc_type_id: str | None = Field(nullable=True, foreign_key='doc_type.id')
    doc_no: str | None = Field(nullable=True)

class DocArchiveFullBase(BaseULIDModel, DocArchiveBase):
    pass

class DocArchive(DocArchiveFullBase, table=True):
    column_types: list["ColumnType"] = Relationship(back_populates="doc_archives", link_model=DocArchiveKolomLink, sa_relationship_kwargs={"lazy": "select"})
    
    