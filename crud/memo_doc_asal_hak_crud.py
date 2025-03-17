from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import (
    MemoDocAsalHak
)
from schemas.memo_doc_asal_hak_sch import MemoDocAsalHakCreateSch, MemoDocAsalHakUpdateSch

class CRUDMemoDocAsalHak(CRUDBase[MemoDocAsalHak, MemoDocAsalHakCreateSch, MemoDocAsalHakUpdateSch]):
    pass

memo_doc_asal_hak = CRUDMemoDocAsalHak(MemoDocAsalHak)