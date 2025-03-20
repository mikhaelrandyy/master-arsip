from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi_pagination.ext.sqlalchemy import paginate
from schemas.oauth import AccessToken
from sqlmodel import and_, select, or_, func
from crud.base_crud import CRUDBase
from models import DocTypeGroup
from schemas.common_sch import OrderEnumSch
from schemas.doc_type_group_sch import DocTypeGroupCreateSch, DocTypeGroupUpdateSch
from common.generator import generate_code
from common.enum import CodeCounterEnum


class CRUDDocTypeGroup(CRUDBase[DocTypeGroup, DocTypeGroupCreateSch, DocTypeGroupUpdateSch]):
  async def get_by_id(self, *, id:str) -> DocTypeGroup:

      query = select(DocTypeGroup)
      query = query.where(DocTypeGroup.id == id)
      response = await db.session.execute(query)
      return response.scalar_one_or_none()
     
  async def create(self, *, sch:DocTypeGroupCreateSch, created_by:str) -> DocTypeGroup:

      sch.code = await generate_code(entity=CodeCounterEnum.DOC_TYPE_GROUP)

      doc_type_group = DocTypeGroup.model_validate(sch)
      if created_by:
          doc_type_group.created_by = doc_type_group.updated_by = created_by

      db.session.add(doc_type_group)
            
      await db.session.commit()
      await db.session.refresh(doc_type_group)

      return doc_type_group
    
  async def get_paginated(self, *, params, login_user: AccessToken | None = None, **kwargs):
      query = self.base_query()
      query = self.create_filter(query=query, login_user=login_user, filter=kwargs)

      return await paginate(db.session, query, params)
    
  async def get_no_paginated(self, *, login_user: AccessToken | None = None, **kwargs):
      query = self.base_query()
      query = self.create_filter(query=query, filter=kwargs, login_user=login_user)
      response = await db.session.execute(query)
      
      return response.scalars().all()
    
  def create_filter(self, *, login_user: AccessToken | None = None, query, filter: dict):
      if filter.get("search"):
         search = filter.get("search")
         query = query.filter(
                  or_(
                     DocTypeGroup.code.ilike(f'%{search}%'),
                     DocTypeGroup.name.ilike(f'%{search}%')
                  )
               )
         
      if filter.get("order_by"):
         if filter.get("order"):
            order_column = getattr(DocTypeGroup, filter.get('order_by'), None)
            if order_column is None:
                raise HTTPException(status_code=400, detail=f'Field {filter.get("order_by")} not found')
            order = filter.get("order")
            if order == OrderEnumSch.descendent:
                  query = query.order_by(order_column.desc())
            if order == OrderEnumSch.ascendent:
                  query = query.order_by(order_column.asc())
      
      return query
    
  def base_query(self):
      query = select(DocTypeGroup)
      return query

    
doc_type_group = CRUDDocTypeGroup(DocTypeGroup)
