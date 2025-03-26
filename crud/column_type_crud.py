from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi_pagination.ext.sqlalchemy import paginate
from schemas.oauth import AccessToken
from sqlmodel import and_, select, or_
from crud.base_crud import CRUDBase
from models import ColumnType
from schemas.common_sch import OrderEnumSch
from schemas.column_type_sch import ColumnTypeCreateSch, ColumnTypeUpdateSch
from common.enum import DataTypeEnum
import crud

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
    
    async def get_paginated(self, *, params, login_user: AccessToken | None = None, **kwargs):
      query = self.base_query()
      query = self.create_filter(query=query, login_user=login_user, filter=kwargs)
      return await paginate(db.session, query, params)
    
    async def get_no_paginated(self, *, login_user: AccessToken | None = None, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs, login_user=login_user)
        response = await db.session.execute(query)

        return response.scalars().all()
    
    def base_query(self):
      query = select(ColumnType)
      return query

    def create_filter(self, *, login_user: AccessToken | None = None, query, filter: dict):
      if filter.get("search"):
         search = filter.get("search")
         query = query.filter(
                  or_(
                     ColumnType.name.ilike(f'%{search}%'),
                     ColumnType.data_type.ilike(f'%{search}%')
                  )
               )
         
      if filter.get("order_by"):
         if filter.get("order"):
            order_column = getattr(ColumnType, filter.get('order_by'), None)
            if order_column is None:
                raise HTTPException(status_code=400, detail=f'Field {filter.get("order_by")} not found')
            order = filter.get("order")
            if order == OrderEnumSch.descendent:
                  query = query.order_by(order_column.desc())
            if order == OrderEnumSch.ascendent:
                  query = query.order_by(order_column.asc())
      
      return query
    
     
column_type = CRUDColumnType(ColumnType)
