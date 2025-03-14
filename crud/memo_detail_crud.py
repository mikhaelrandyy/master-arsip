from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models.memo_doc_model import MemoDoc
from schemas.doc_detail_sch import MemoDocCreateSch, MemoDocUpdateSch


class CRUDMemoDetail(CRUDBase[MemoDoc, MemoDocCreateSch, MemoDocUpdateSch]):
    async def get_by_id(self, *, id:str) -> MemoDoc:

        query = select(MemoDoc)
        query = query.where(MemoDoc.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()

memo_detail = CRUDMemoDetail(MemoDoc)
