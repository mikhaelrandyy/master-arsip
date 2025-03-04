from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import ColumnType
from schemas.column_type_sch import ColumnTypeCreateSch, ColumnTypeUpdateSch


class CRUDColumnType(CRUDBase[ColumnType, ColumnTypeCreateSch, ColumnTypeUpdateSch]):
    async def get_by_id(self, *, id:str) -> ColumnType:

        query = select(ColumnType)
        query = query.where(ColumnType.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
column_type = CRUDColumnType(ColumnType)
