from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocTypeColumn, ColumnType, DocType
from schemas.doc_type_sch import DocTypeSch
from schemas.doc_type_column_sch import DocTypeColumnSch, DocTypeColumnCreateSch, DocTypeColumnUpdateSch, DocTypeColumnCreateUpdateSch
import crud


class CRUDDocTypeColumn(CRUDBase[DocTypeColumnSch, DocTypeColumnCreateSch, DocTypeColumnUpdateSch]):
    async def get_by_doc_type(self, *, doc_type_id:str) -> list[DocTypeColumn]:

        query = select(DocTypeColumn)
        query = query.where(DocTypeColumn.doc_type_id == doc_type_id)
        response = await db.session.execute(query)
        return response.scalars().all()

    async def get_doc_type_column(self, *, doc_type_id: str, column_type_id:str) -> DocTypeColumn:

        query = select(DocTypeColumn)
        query = query.where(and_(DocTypeColumn.doc_type_id == doc_type_id,
                                 DocTypeColumn.column_type_id == column_type_id))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()

    def base_query(self):
        query = select(
            *DocTypeColumn.__table__.columns,
            ColumnType.name.label('column_name'),
            DocType.name.label('doc_type_name')
        )

        query = query.join(ColumnType, ColumnType.id == DocTypeColumn.column_type_id
                    ).join(DocType, DocType.id == DocTypeColumn.doc_type_id)
        
        return query

    async def fetch_column_by_doc_type(self, doc_type_id: str):
        query = self.base_query()
        query = query.filter(DocTypeColumn.doc_type_id == doc_type_id)
        response = await db.session.execute(query)

        return response.mappings().all()

doc_type_column = CRUDDocTypeColumn(DocTypeColumn)
