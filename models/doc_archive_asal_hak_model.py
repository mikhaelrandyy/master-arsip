from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocArchive


class DocArchiveAsalHakBase(SQLModel):
    doc_archive_id: str | None = Field(nullable=False, foreign_key='doc_archive.id')
    doc_archive_asal_id: str | None = Field(nullable=False, foreign_key='doc_archive.id')

class DocArchiveAsalHakFullBase(BaseULIDModel, DocArchiveAsalHakBase):
    pass

class DocArchiveAsalHak(DocArchiveAsalHakFullBase, table=True):
    doc_archive: "DocArchive" = Relationship(sa_relationship_kwargs={"lazy": "select"})