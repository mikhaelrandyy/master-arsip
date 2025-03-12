from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models.memo_detail_model import MemoDetail
from schemas.doc_detail_sch import MemoDetailCreateSch, MemoDetailUpdateSch


class CRUDMemoDetail(CRUDBase[MemoDetail, MemoDetailCreateSch, MemoDetailUpdateSch]):
    async def get_by_id(self, *, id:str) -> MemoDetail:

        query = select(MemoDetail)
        query = query.where(MemoDetail.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()

memo_detail = CRUDMemoDetail(MemoDetail)
