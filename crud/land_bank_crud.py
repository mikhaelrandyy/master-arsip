from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_async_sqlalchemy import db
from sqlmodel import select, or_, cast, func, Integer, case, Numeric
from sqlalchemy.orm import aliased
from crud.base_crud import CRUDBase
from models import LandBank, Project, Desa, Company, Alashak
from schemas.land_bank_sch import LandBankCreateSch, LandBankUpdateSch
from schemas.common_sch import OrderEnumSch
from schemas.oauth import AccessToken
from common.enum import CodeCounterEnum
import crud
from datetime import datetime

class CRUDLandBank(CRUDBase[LandBank, LandBankCreateSch, LandBankUpdateSch]):
    async def create_land_bank(self, *, sch:LandBankCreateSch, created_by:str) -> LandBank:
        db_obj = LandBank.model_validate(sch)
        db_obj.code = await self.generate_code(sch=sch)

        if created_by:
            db_obj.created_by = db_obj.updated_by = created_by

        db.session.add(db_obj)

        await db.session.commit()
        await db.session.refresh(db_obj)

        return db_obj
    
    async def generate_code(self, *, sch:LandBankCreateSch):
        project = await crud.project.get(id=sch.project_id)
        desa = await crud.desa.get(id=sch.desa_id)
        last_land_bank = await self.get_last(parent_id=sch.parent_id)
        
        if sch.parent_id is None:
            prefix = f"L-{datetime.today().year}-{project.code}-{desa.code}."
            code = f"{prefix}{int(last_land_bank.code.split('.')[-1]) + 1:05d}" if last_land_bank else f"{prefix}{1:05d}"
        else:
            parent_land_bank = await self.get(id=sch.parent_id)
            code = f"{parent_land_bank.code}.{int(last_land_bank.code.split('.')[-1]) + 1}" if last_land_bank else f"{parent_land_bank.code}.{1}"

        return code
   
    async def get_last(self, *, parent_id: str | None = None) -> LandBank | None:
        response = await db.session.execute(select(LandBank).where(LandBank.parent_id == parent_id).order_by(LandBank.created_at.desc()).limit(1))
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

        ParentLandBank = aliased(LandBank)

        total_luas_tanah = (
            select(
                LandBank.parent_id.label('parent_id'),
                func.sum(func.coalesce(LandBank.luas_tanah, 0)).label('total_luas')
            )
            .where(LandBank.parent_id != None)
            .group_by(LandBank.parent_id).cte("total_luas_cte")
        )
        
        query = select(
                    *LandBank.__table__.columns,
                    Project.name.label('project_name'),
                    Project.code.label('project_code'),
                    Company.name.label('company_name'),
                    Company.code.label('company_code'),
                    Desa.name.label('desa_name'),
                    Alashak.name.label('alashak_name'),
                    ParentLandBank.code.label('parent_code'),
                    case((LandBank.parent_id == None, total_luas_tanah.c.total), else_=None).label('luas_pemisah'),
                    case((LandBank.parent_id == None, LandBank.luas_tanah - func.coalesce(total_luas_tanah.c.total, 0)), else_=None).label("sisa_luas")
                )

        query = query.outerjoin(Project, Project.id == LandBank.project_id
                    ).outerjoin(Desa, Desa.id == LandBank.desa_id
                    ).outerjoin(Company, Company.id == LandBank.company_id
                    ).outerjoin(Alashak, Alashak.id == LandBank.alashak_id
                    ).outerjoin(ParentLandBank, ParentLandBank.parent_id == LandBank.id
                    ).outerjoin(total_luas_tanah, total_luas_tanah.c.parent_id == 
                        case(
                            (LandBank.parent_id != None, LandBank.parent_id),
                            else_=LandBank.id
                        )
                    )
    
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
