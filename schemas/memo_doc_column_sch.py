from sqlmodel import SQLModel
from models.memo_doc_column_model import MemoDocColumnBase, MemoDocColumnFullBase
from common.enum import DataTypeEnum

class MemoDocColumnCreateSch(MemoDocColumnBase):
    pass

class MemoDocColumnSch(MemoDocColumnFullBase):
    column_type_name: str | None = None 
    data_type: DataTypeEnum | None = None
    enum_data: str | None = None
    is_mandatory: bool | None = None

class MemoDocColumnUpdateSch(MemoDocColumnBase):
    id: str | None = None

