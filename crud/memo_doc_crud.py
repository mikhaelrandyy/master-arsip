from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import (
    MemoDoc,
    DocType,
    Unit,
    Alashak
)
from schemas.memo_doc_sch import MemoDocCreateSch, MemoDocUpdateSch
from schemas.oauth import AccessToken
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
    
    async def fetch_by_memo(self, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs)
        response = await db.session.execute(query)
        return response.mappings().all()
    
    def base_query(self):

        query = select(
            *MemoDoc.__table__.columns,
            Unit.code.label("unit_code"),
            Unit.descs.label("unit_descs"),
            Alashak.code.label("alashak_code"),
            Alashak.name.label("alashak_name")
        )
        query = query.outerjoin(DocType, DocType.id == MemoDoc.doc_type_id
                    ).outerjoin(Unit, Unit.id == MemoDoc.unit_id
                    ).outerjoin(Alashak, Alashak.id == MemoDoc.alashak_id)

        return query

    def create_filter(self, *, query, filter:dict):

        if filter.get("memo_id"):
            query = query.where(MemoDoc.memo_id == filter.get("memo_id"))

        return query

memo_doc = CRUDMemoDoc(MemoDoc)