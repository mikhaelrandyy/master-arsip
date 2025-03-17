from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import (
    MemoDocColumn
)
from schemas.memo_doc_column_sch import MemoDocColumnCreateSch, MemoDocColumnUpdateSch

class CRUDMemoDocColumn(CRUDBase[MemoDocColumn, MemoDocColumnCreateSch, MemoDocColumnUpdateSch]):
    pass

memo_doc_column = CRUDMemoDocColumn(MemoDocColumn)