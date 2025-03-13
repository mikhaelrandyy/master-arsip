from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from models.doc_archive_column_model import DocArchiveColumn
from typing import TYPE_CHECKING
from common.enum import TypeDocFisikEnum, JenisArsipEnum, StatusDocArchiveEnum


if TYPE_CHECKING:
    from models import DocArchive

class DocArchiveAttachmentBase(SQLModel):
    doc_archive_id: str | None = Field(nullable=True, foreign_key='doc_archive.id')
    file_name: str | None = Field(nullable=True)
    file_url: str | None = Field(nullable=True)

class DocArchiveAttachmentFullBase(BaseULIDModel, DocArchiveAttachmentBase):
    pass

class DocArchiveAttachment(DocArchiveAttachmentFullBase, table=True):
    doc_archive: "DocArchive" = Relationship(sa_relationship_kwargs={"lazy": "select"})
     
    