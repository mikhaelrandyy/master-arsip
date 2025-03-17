from sqlmodel import SQLModel
from models.memo_doc_column_model import MemoDocColumnBase, MemoDocColumnFullBase

class MemoDocColumnCreateSch(MemoDocColumnBase):
    pass

class MemoDocColumnSch(MemoDocColumnFullBase):
    pass 

class MemoDocColumnUpdateSch(MemoDocColumnBase):
    id: str | None = None

class MemoDocColumnByIdSch(MemoDocColumnFullBase):
    pass
