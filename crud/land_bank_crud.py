from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_async_sqlalchemy import db
from sqlmodel import select, or_, cast, func, Integer, desc
from crud.base_crud import CRUDBase
from models import LandBank, Project, Desa, Company
from schemas.land_bank_sch import LandBankCreateSch, LandBankUpdateSch
from schemas.common_sch import OrderEnumSch
from schemas.oauth import AccessToken
from common.enum import CodeCounterEnum
import crud
from datetime import datetime

class CRUDLandBank(CRUDBase[LandBank, LandBankCreateSch, LandBankUpdateSch]):
    async def create_land_bank(self, *, sch:LandBankCreateSch, created_by:str) -> LandBank:
        
        year = datetime.today().year
        project = await crud.project.get(id=sch.project_id)
        desa = await crud.desa.get(id=sch.desa_id)
        
        if sch.parent_id is None:

            land_bank = await self.get_last_code_for_land_bank()
            parent = await crud.land_bank.get(id=land_bank)

            parent_code = 0

            if land_bank:
                current_code = int(parent.code.split('.')[-1])
                sch.code = f"L-{year}-{project.code}-{desa.code}.{current_code + 1:05d}"
            else:
                sch.code = f"L-{year}-{project.code}-{desa.code}.{parent_code + 1:05d}"

        else:

            land_bank = await self.get_last_code_for_land_bank(parent_id=sch.parent_id)
            parent = await crud.land_bank.get(id=land_bank)

            child_code = 0

            if land_bank:
                current_children = int(parent.code.split('.')[-1])
                current_parent = parent.code.split('.')[1]
                sch.code = f"L-{year}-{project.code}-{desa.code}.{current_parent}.{current_children + 1}"
            else:
                sch.code = f"{parent.code}.{child_code + 1}"

        # db_obj = LandBank(**sch.model_dump())

        db_obj = LandBank.model_validate(sch)

        if created_by:
            db_obj.created_by = db_obj.updated_by = created_by

        db.session.add(db_obj)

        await db.session.commit()
        await db.session.refresh(db_obj)

        return db_obj
   
    async def get_last_code_for_land_bank(self, *, parent_id: str | None = None) -> LandBank:
       
        query = self.base_query()

        if parent_id:
            query = query.filter(LandBank.parent_id.ilike(f"%{parent_id}%"))
            query = query.order_by(LandBank.created_at.desc()).limit(1)
        else:
            query = query.filter(LandBank.parent_id == None)
            query = query.order_by(LandBank.code.desc()).limit(1)

        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def get_by_id(self, *, id:str):
        land_bank = await self.fetch_land_bank(id=id)
        if not land_bank: 
            return None
        
        return land_bank
    
    async def fetch_land_bank(self, id: str):
        query = self.base_query()
        query = query.where(LandBank.id == id)
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

        return response.mappings().all()

    def base_query(self):

        query = select(
                    *LandBank.__table__.columns,
                    Project.code.label('project_code'),
                    Company.code.label('company_code')
                )

        query = query.outerjoin(Project, Project.id == LandBank.project_id
                    ).outerjoin(Desa, Desa.id == LandBank.desa_id
                    ).outerjoin(Company, Company.id == LandBank.company_id)

        return query
   
    def create_filter(self, *, login_user: AccessToken | None = None, query, filter: dict):
       if filter.get("search"):
          search = filter.get("search")
          query = query.filter(
                    or_(
                       LandBank.code.ilike(f'%{search}%'),
                       LandBank.doc_no.ilike(f'%{search}%')
                    )
                 )

       if filter.get("order_by"):
          if filter.get("order"):
             order_column = getattr(LandBank, filter.get('order_by'), None)
             if order_column is None:
                raise HTTPException(status_code=400, detail=f'Field {filter.get("order_by")} not found')
             order = filter.get("order")
             if order == OrderEnumSch.descendent:
                   query = query.order_by(order_column.desc())
             if order == OrderEnumSch.ascendent:
                   query = query.order_by(order_column.asc())

       return query

land_bank = CRUDLandBank(LandBank)
