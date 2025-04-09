from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import (
    MemoDoc,
    MemoDocAsalHak
)
from schemas.memo_doc_asal_hak_sch import MemoDocAsalHakCreateSch, MemoDocAsalHakUpdateSch

class CRUDMemoDocAsalHak(CRUDBase[MemoDocAsalHak, MemoDocAsalHakCreateSch, MemoDocAsalHakUpdateSch]):
    async def get_by_memo(self, *, memo_id:str) -> list[MemoDocAsalHak]:

        query = select(MemoDocAsalHak
                    ).join(MemoDoc, MemoDoc.id == MemoDocAsalHak.memo_doc_id
                    ).where(MemoDoc.memo_id == memo_id)
        
        response = await db.session.execute(query)
        return response.scalars().all()
    
    async def get_by_memo_doc(self, *, memo_doc_id:str) -> list[MemoDocAsalHak]:

        query = select(MemoDocAsalHak).where(MemoDocAsalHak.memo_doc_id == memo_doc_id)
        
        response = await db.session.execute(query)
        return response.scalars().all()
    
    async def fetch_by_memo_doc(self, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs)

        response = await db.session.execute(query)
        return response.mappings().all()

    
    def base_query(self):
        return select(*MemoDocAsalHak.__table__.columns)
    
    def create_filter(self, query, filter:dict):
        if filter.get("memo_doc_id"):
            query = query.where(MemoDocAsalHak.memo_doc_id == filter.get("memo_doc_id"))

        return query

memo_doc_asal_hak = CRUDMemoDocAsalHak(MemoDocAsalHak)