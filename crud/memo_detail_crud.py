from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models.memo_dt_model import MemoDt
from schemas.doc_detail_sch import MemoDetailCreateSch, MemoDetailUpdateSch


class CRUDMemoDetail(CRUDBase[MemoDt, MemoDetailCreateSch, MemoDetailUpdateSch]):
    async def get_by_id(self, *, id:str) -> MemoDt:

        query = select(MemoDt)
        query = query.where(MemoDt.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()

memo_detail = CRUDMemoDetail(MemoDt)
