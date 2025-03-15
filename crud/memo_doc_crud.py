from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models.memo_doc_model import MemoDoc
from schemas.memo_doc_sch import MemoDocCreateSch, MemoDocUpdateSch
from models.memo_model import Memo


class CRUDMemoDoc(CRUDBase[MemoDoc, MemoDocCreateSch, MemoDocUpdateSch]):
    async def get_by_id(self, *, id:str) -> MemoDoc:

        query = self.base_query()
        query = query.where(MemoDoc.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def get_by_memo(self, *, memo_id:str) -> list[MemoDoc]:

        query = select(MemoDoc)
        query = query.where(MemoDoc.memo_id == memo_id)
        response = await db.session.execute(query)
        return response.scalars().all()
    
    async def fetch_memo_id(self, memo_id:str):
        query = self.base_query()
        query = query.where(MemoDoc.memo_id == memo_id)
        response = await db.session.execute(query)
        return response.mappings().all()
    
    def base_query(self):

        query = select(MemoDoc)
        query = query.join(Memo, Memo.id == MemoDoc.memo_id)

        return query

memo_doc = CRUDMemoDoc(MemoDoc)