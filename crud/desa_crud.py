from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_async_sqlalchemy import db
from sqlmodel import select, or_
from crud.base_crud import CRUDBase
from models.desa_model import Desa
from schemas.desa_sch import DesaCreateSch, DesaUpdateSch
from schemas.common_sch import OrderEnumSch
from schemas.oauth import AccessToken


class CRUDDesa(CRUDBase[Desa, DesaCreateSch, DesaUpdateSch]):

   async def get_by_id(self, *, id:str):
      desa = await self.fetch_desa(id=id)
      if not desa: return None
      
      return desa
   
   async def fetch_desa(self, id:str):
        query = self.base_query()
        query = query.where(Desa.id == id)
        response = await db.session.execute(query)
        return response.one_or_none()
   
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

      query = select(Desa)

      return query
   
   def create_filter(self, *, login_user: AccessToken | None = None, query, filter: dict):
      if filter.get("search"):
         search = filter.get("search")
         query = query.filter(
                   or_(
                      Desa.code.ilike(f'%{search}%'),
                      Desa.name.ilike(f'%{search}%')
                   )
                )

      if filter.get("order_by"):
         if filter.get("order"):
            order_column = getattr(Desa, filter.get('order_by'), None)
            if order_column is None:
               raise HTTPException(status_code=400, detail=f'Field {filter.get("order_by")} not found')
            order = filter.get("order")
            if order == OrderEnumSch.descendent:
                  query = query.order_by(order_column.desc())
            if order == OrderEnumSch.ascendent:
                  query = query.order_by(order_column.asc())

      return query

desa = CRUDDesa(Desa)
