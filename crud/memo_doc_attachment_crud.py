from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import (
    MemoDoc,
    MemoDocAttachment
)
from schemas.memo_doc_attachment_sch import MemoDocAttachmentCreateSch, MemoDocAttachmentUpdateSch

class CRUDMemoDocAttachment(CRUDBase[MemoDocAttachment, MemoDocAttachmentCreateSch, MemoDocAttachmentUpdateSch]):
    async def get_by_memo(self, *, memo_id:str) -> list[MemoDocAttachment]:

        query = select(MemoDocAttachment
                    ).join(MemoDoc, MemoDoc.id == MemoDocAttachment.memo_doc_id
                    ).where(MemoDoc.memo_id == memo_id)
        
        response = await db.session.execute(query)
        return response.scalars().all()
    
    async def fetch_by_memo_doc(self, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs)

        response = await db.session.execute(query)
        return response.mappings().all()
    
    def base_query(self):
        return select(*MemoDocAttachment.__table__.columns)
        
    def create_filter(self, *, query, filter:dict):
        if filter.get("memo_doc_id"):
            query = query.where(MemoDocAttachment.memo_doc_id == filter.get("memo_doc_id"))

        return query
    
memo_doc_attachment = CRUDMemoDocAttachment(MemoDocAttachment)