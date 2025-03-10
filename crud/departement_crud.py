from fastapi import HTTPException, status
from fastapi_async_sqlalchemy import db
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import and_, select, or_, func
from crud.base_crud import CRUDBase
from models import Departement, DepartementDocType, DocType
from schemas.departement_sch import DepartementCreateSch, DepartementUpdateSch, DepartementSch, DepartementByIdSch
from schemas.departement_doc_type_sch import DepartementDocTypeCreateSch, DepartementDocTypeSch
from schemas.oauth import AccessToken
import crud

class CRUDDepartement(CRUDBase[Departement, DepartementCreateSch, DepartementUpdateSch]):

   async def get_paginated(self, *, params, login_user: AccessToken | None = None, **kwargs):
      query = self.base_query()
      query = self.create_filter(query=query, login_user=login_user, filter=kwargs)

      return await paginate(db.session, query, params)
   
   async def get_no_page(self, *, login_user: AccessToken | None = None, **kwargs):
      query = self.base_query()
      query = self.create_filter(query=query, login_user=login_user, filter=kwargs)

      response = await db.session.execute(query)
      return response.mappings().all()

   async def get_by_id(self, *, id: str):
      departement = await self.fetch_departement(id=id)
      if not departement: return None

      departement = DepartementByIdSch(**departement._mapping)
      departement.doc_types = await self.fetch_departement_doc_types(departement_id=id)

      return departement

   async def update_and_mapping_w_doc_type(self, *, obj_current: Departement, doc_type_ids: list[str] | None = []):
      current_departement_doc_types = await crud.departement_doc_type.get_by_departement(departement_id=obj_current.id)
      
      for doc_type_id in doc_type_ids:
         departement_doc_type = await crud.departement_doc_type.get_departement_doc_type(departement_id=obj_current.id, doc_type_id=doc_type_id)
         if not departement_doc_type:
            doc_type = await crud.doc_type.get(id=doc_type_id)
            if not doc_type:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selected document type not found!")
            
            db_obj = DepartementDocType(doc_type_id=doc_type_id, departement_id=obj_current.id)
            db.session.add(db_obj)
            await db.session.flush()
         else:
            current_departement_doc_types.remove(departement_doc_type)

      for current_departement_doc_type in current_departement_doc_types:
         await db.session.delete(current_departement_doc_type)

      await db.session.commit()

   def base_query(self):

      count_doc_types_sq = (
            select(func.count(Departement.id).label("jmlh"), Departement.id
                ).join(DepartementDocType, DepartementDocType.departement_id == Departement.id
                ).group_by(Departement.id).cte("number_of_doc_types_cte")
        )

      query = select(
         *Departement.__table__.columns,
         count_doc_types_sq.c.jmlh.label("number_of_doc_types")

      )
      query = query.outerjoin(DepartementDocType, Departement.id == DepartementDocType.departement_id
                  ).outerjoin(DocType, DocType.id == DepartementDocType.doc_type_id
                  ).outerjoin(count_doc_types_sq, count_doc_types_sq.c.id == Departement.id)
      
      query = query.distinct()

      return query
   
   def create_filter(self, *, login_user: AccessToken | None = None, query, filter: dict):
      if filter.get("search"):
         search = filter.get("search")
         query = query.filter(
                  or_(
                     Departement.code.ilike(f'%{search}%'),
                     Departement.name.ilike(f'%{search}%')
                  )
               )
         
      if filter.get("order_by"):
            order_column = getattr(Departement, filter.get('order_by'))
            query = query.order_by(order_column.desc())

      return query

   async def fetch_departement(self, id: str):
      query = self.base_query()
      query = query.where(Departement.id == id)

      response = await db.session.execute(query)
      return response.one_or_none()

   async def fetch_departement_doc_types(self, departement_id: str):
      dept_doc_types = await crud.departement_doc_type.fetch_column_by_departement(departement_id=departement_id)
      if not dept_doc_types: return []

      departement_doc_types = []
      for dept_doc_type in departement_doc_types:
         dept_doc_typ = DepartementDocTypeSch(**dept_doc_type)
         departement_doc_types.append(dept_doc_typ)

      return departement_doc_types

departement = CRUDDepartement(Departement)
