from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import MemoDoc, ColumnType

class MemoDocColumnBase(SQLModel):
    memo_doc_id: str | None = Field(nullable=True, foreign_key='memo_doc.id', default=None)
    column_type_id: str | None = Field(nullable=True, foreign_key='column_type.id')
    value: str | None = Field(nullable=True)

class MemoDocColumnFullBase(BaseULIDModel, MemoDocColumnBase):
    pass

class MemoDocColumn(MemoDocColumnFullBase, table=True):pass 

    


    
    