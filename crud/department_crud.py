from fastapi import HTTPException, status
from fastapi_async_sqlalchemy import db
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.encoders import jsonable_encoder
from sqlmodel import and_, select, or_, func
from crud.base_crud import CRUDBase
from models import Department, DepartmentDocType, DocType
from schemas.common_sch import OrderEnumSch
from schemas.department_sch import DepartmentCreateSch, DepartmentUpdateSch, DepartmentSch, DepartmentByIdSch
from schemas.department_doc_type_sch import DepartmentDocTypeCreateSch, DepartmentDocTypeSch
from schemas.oauth import AccessToken
import crud

class CRUDDepartment(CRUDBase[Department, DepartmentCreateSch, DepartmentUpdateSch]):
   async def create_w_doc_type(self, *, obj_in: DepartmentCreateSch, created_by: str):
      db_obj = Department(**obj_in.model_dump())
      if created_by:
            db_obj.created_by = db_obj.updated_by = created_by

      db.session.add(db_obj)
      await db.session.flush()

      for obj in obj_in.doc_type_ids:
         db_obj_map = DepartmentDocType(doc_type_id=obj, department_id=db_obj.id)
         db.session.add(db_obj_map)

      await db.session.commit()
      await db.session.refresh(db_obj)

      return db_obj
   
   async def update_w_doc_type(self, *, obj_current: Department, obj_new: DepartmentUpdateSch, updated_by: str):
      obj_data = jsonable_encoder(obj_current)
      update_data = obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)

      for field in obj_data:
         if field in update_data:
               setattr(obj_current, field, update_data[field])
         elif updated_by and updated_by != "" and field == "updated_by":
               setattr(obj_current, field, updated_by)

      db.session.add(obj_current)
      await db.session.flush()
      
      current_department_doc_types = await crud.department_doc_type.get_by_department(department_id=obj_current.id)
      
      for doc_type_id in obj_new.doc_type_ids:
         department_doc_type = await crud.department_doc_type.get_department_doc_type(department_id=obj_current.id, doc_type_id=doc_type_id)
         if not department_doc_type:
            doc_type = await crud.doc_type.get(id=doc_type_id)
            if not doc_type:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selected document type not found!")
            
            db_obj = DepartmentDocType(doc_type_id=doc_type_id, department_id=obj_current.id)
            db.session.add(db_obj)
            await db.session.flush()
         else:
            current_department_doc_types.remove(department_doc_type)

      for current_department_doc_type in current_department_doc_types:
         await db.session.delete(current_department_doc_type)

      await db.session.commit()

   async def get_paginated(self, *, params, login_user: AccessToken | None = None, **kwargs):
      query = self.base_query()
      query = self.create_filter(query=query, login_user=login_user, filter=kwargs)

      return await paginate(db.session, query, params)
   
   async def get_no_paginated(self, *, login_user: AccessToken | None = None, **kwargs):
      query = self.base_query()
      query = self.create_filter(query=query, login_user=login_user, filter=kwargs)

      response = await db.session.execute(query)
      return response.mappings().all()

   async def get_by_id(self, *, id: str):
      department = await self.fetch_department(id=id)
      if not department: return None

      department = DepartmentByIdSch(**department._mapping)
      department.doc_types = await self.fetch_department_doc_types(department_id=id)

      return department

   def base_query(self):

      count_doc_types_sq = (
            select(func.count(Department.id).label("jmlh"), Department.id
                ).join(DepartmentDocType, DepartmentDocType.department_id == Department.id
                ).group_by(Department.id).cte("number_of_doc_types_cte")
        )

      query = select(
         *Department.__table__.columns,
         count_doc_types_sq.c.jmlh.label("number_of_doc_types")

      )
      query = query.outerjoin(DepartmentDocType, Department.id == DepartmentDocType.department_id
                  ).outerjoin(DocType, DocType.id == DepartmentDocType.doc_type_id
                  ).outerjoin(count_doc_types_sq, count_doc_types_sq.c.id == Department.id)
      
      query = query.distinct()

      return query
   
   def create_filter(self, *, login_user: AccessToken | None = None, query, filter: dict):
      if filter.get("search"):
         search = filter.get("search")
         query = query.filter(
                  or_(
                     Department.code.ilike(f'%{search}%'),
                     Department.name.ilike(f'%{search}%')
                  )
               )
         
      if filter.get("order_by"):
         if filter.get("order"):
            order_column = getattr(Department, filter.get('order_by'), None)
            if order_column is None:
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Field {filter.get("order_by")} not found')
            order = filter.get("order")
            if order == OrderEnumSch.descendent:
                  query = query.order_by(order_column.desc())
            if order == OrderEnumSch.ascendent:
                  query = query.order_by(order_column.asc())
      
      return query

   async def fetch_department(self, id: str):
      query = self.base_query()
      query = query.where(Department.id == id)

      response = await db.session.execute(query)
      return response.one_or_none()

   async def fetch_department_doc_types(self, department_id: str):
      dept_doc_types = await crud.department_doc_type.fetch_column_by_department(department_id=department_id)
      if not dept_doc_types: return []

      department_doc_types = []
      for dept_doc_type in department_doc_types:
         dept_doc_typ = DepartmentDocTypeSch(**dept_doc_type)
         department_doc_types.append(dept_doc_typ)

      return department_doc_types

department = CRUDDepartment(Department)
