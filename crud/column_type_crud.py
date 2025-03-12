from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import ColumnType
from schemas.column_type_sch import ColumnTypeCreateSch, ColumnTypeUpdateSch
from common.enum import DataTypeEnum


class CRUDColumnType(CRUDBase[ColumnType, ColumnTypeCreateSch, ColumnTypeUpdateSch]):
    async def get_by_id(self, *, id:str) -> ColumnType:

        query = select(ColumnType)
        query = query.where(ColumnType.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create(self, *, sch:ColumnTypeCreateSch, created_by:str) -> ColumnType:

        if sch.data_type == DataTypeEnum.ENUM:
            if sch.enum_data is None:
                raise HTTPException(status_code=400, detail="Enum data is required for Tipe Data Enum")

        column_type = ColumnType.model_validate(sch)

        if created_by:
            column_type.created_by = column_type.updated_by = created_by

        db.session.add(column_type)
        await db.session.commit()
        await db.session.refresh(column_type)

        return column_type
     
column_type = CRUDColumnType(ColumnType)
