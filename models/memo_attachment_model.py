from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Unit, Company

class MemoAttachmentBase(SQLModel):
    memo_dt_id: str | None = Field(nullable=False, foreign_key='memo_detail.id')
    file_url: str | None = Field(nullable=False)

class MemoAttachmentFullBase(BaseULIDModel, MemoAttachmentBase):
    pass

class MemoAttachment(MemoAttachmentFullBase, table=True):
    pass


    
    