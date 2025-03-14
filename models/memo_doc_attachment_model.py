from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import MemoDoc

class MemoDocAttachmentBase(SQLModel):
    memo_doc_id: str | None = Field(nullable=False, foreign_key='memo_doc.id')
    file_name: str | None = Field(nullable=True)
    file_url: str | None = Field(nullable=True)

class MemoDocAttachmentFullBase(BaseULIDModel, MemoDocAttachmentBase):
    pass

class MemoDocAttachment(MemoDocAttachmentFullBase, table=True):
    pass


    
    