from sqlmodel import SQLModel
from models.memo_doc_column_model import MemoDocColumnBase, MemoDocColumnFullBase
from common.enum import DataTypeEnum

class MemoDocColumnCreateSch(MemoDocColumnBase):
    pass

class MemoDocColumnSch(MemoDocColumnFullBase):
    column_name: str | None = None 
    column_data_type: DataTypeEnum | None = None
    column_enum_data: str | None = None
    column_is_mandatory: bool | None = None

class MemoDocColumnUpdateSch(MemoDocColumnBase):
    id: str | None = None

