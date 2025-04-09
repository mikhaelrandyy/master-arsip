from models.base_model import BaseULIDModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field

class DocArchiveHistoryBase(SQLModel):
    doc_archive_id: str = Field(nullable=True, foreign_key='doc_archive.id')
    memo_id: str = Field(nullable=True, foreign_key='memo.id')
    before: dict = Field(sa_type=JSONB, nullable=True)
    after: dict = Field(sa_type=JSONB, nullable=True)
    
class DocArchiveHistoryFullBase(BaseULIDModel, DocArchiveHistoryBase):
    pass

class DocArchiveHistory(DocArchiveHistoryFullBase, table=True):
    pass


    