from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import (
    MemoDoc,
    MemoDocColumn,
    ColumnType
)
from schemas.memo_doc_column_sch import MemoDocColumnCreateSch, MemoDocColumnUpdateSch

class CRUDMemoDocColumn(CRUDBase[MemoDocColumn, MemoDocColumnCreateSch, MemoDocColumnUpdateSch]):
    async def get_by_memo(self, *, memo_id:str) -> list[MemoDocColumn]:

        query = select(MemoDocColumn
                    ).join(MemoDoc, MemoDoc.id == MemoDocColumn.memo_doc_id
                    ).where(MemoDoc.memo_id == memo_id)
        
        response = await db.session.execute(query)
        return response.scalars().all()
    
    async def fetch_by_memo_doc(self, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs)

        response = await db.session.execute(query)
        return response.mappings().all()
    
    def base_query(self):

        query = select(
            *MemoDocColumn.__table__.columns,
            ColumnType.name.label("column_type_name"),
            ColumnType.data_type,
            ColumnType.enum_data,
            ColumnType.is_mandatory
        )
        query = query.outerjoin(ColumnType, ColumnType.id == MemoDocColumn.column_type_id)

        return query
    
    def create_filter(self, *, query, filter:dict):
        if filter.get("memo_doc_id"):
            query = query.where(MemoDocColumn.memo_doc_id == filter.get("memo_doc_id"))

        return query
        

memo_doc_column = CRUDMemoDocColumn(MemoDocColumn)