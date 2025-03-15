from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models.memo_doc_model import MemoDoc
from schemas.doc_detail_sch import MemoDocCreateSch, MemoDocUpdateSch
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
    
    async def get_by_memo_id_w_memo_doc_id(self, *, memo_id: str, memo_doc_id:str, doc_archive_id:str) -> MemoDoc:

        query = select(MemoDoc)
        query = query.where(and_(MemoDoc.memo_id == memo_id,
                                 MemoDoc.id == memo_doc_id,
                                 MemoDoc.doc_archive_id == doc_archive_id))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
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