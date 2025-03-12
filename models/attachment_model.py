from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Unit, Company

class AttachmentBase(SQLModel):
    memo_dt_id: str | None = Field(nullable=True, foreign_key='memo_detail.id')
    file_path: str | None = Field(nullable=True)

class AttachmentFullBase(BaseULIDModel, AttachmentBase):
    pass

class Attachment(AttachmentFullBase, table=True):
    pass


    
    