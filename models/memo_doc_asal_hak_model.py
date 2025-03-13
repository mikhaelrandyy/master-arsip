from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import MemoDoc
    
class MemoDocAsalHakBase(SQLModel):
    memo_doc_id: str | None = Field(nullable=True, foreign_key='memo_doc.id')
    doc_archive_asal_id: str | None = Field(nullable=True)

class MemoDocAsalHakFullBase(BaseULIDModel, MemoDocAsalHakBase):
    pass

class MemoDocAsalHak(MemoDocAsalHakFullBase, table=True):
    memo_doc: "MemoDoc" = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    


    
    