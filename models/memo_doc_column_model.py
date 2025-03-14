from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import MemoDoc, ColumnType

class MemoDocAttachmentBase(SQLModel):
    memo_doc_id: str | None = Field(nullable=False, foreign_key='memo_doc.id')
    column_type_id: str | None = Field(nullable=False, foreign_key='column_type.id')
    value: str | None = Field(nullable=True)

class MemoDocAttachmentFullBase(BaseULIDModel, MemoDocAttachmentBase):
    pass

class MemoDocAttachment(MemoDocAttachmentFullBase, table=True):pass

    


    
    