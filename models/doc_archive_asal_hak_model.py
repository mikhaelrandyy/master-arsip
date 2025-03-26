from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field

class DocArchiveAsalHakBase(SQLModel):
    doc_archive_id: str | None = Field(nullable=False, foreign_key='doc_archive.id')
    doc_archive_asal_id: str | None = Field(nullable=False, foreign_key='doc_archive.id')

class DocArchiveAsalHakFullBase(BaseULIDModel, DocArchiveAsalHakBase):
    pass

class DocArchiveAsalHak(DocArchiveAsalHakFullBase, table=True):
    pass