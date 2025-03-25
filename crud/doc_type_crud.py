from fastapi import HTTPException, status
from fastapi_async_sqlalchemy import db
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params, Page
from sqlmodel import and_, select, cast, String, or_, func
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from crud.base_crud import CRUDBase
from models import (
    DocType, 
    DocTypeArchive, 
    DocTypeGroup, 
    DepartmentDocType, 
    Worker, 
    DocTypeColumn
)
from schemas.common_sch import OrderEnumSch
from schemas.oauth import AccessToken
from schemas.doc_type_sch import DocTypeCreateSch, DocTypeUpdateSch, DocTypeSch, DocTypeByIdSch
from schemas.doc_type_archive_sch import DocTypeArchiveCreateSch, DocTypeArchiveSch
from schemas.doc_type_column_sch import DocTypeColumnSch
from common.generator import generate_code
from common.enum import CodeCounterEnum
import crud

class CRUDDocType(CRUDBase[DocType, DocTypeCreateSch, DocTypeUpdateSch]):

    async def create_and_mapping_w_doc_format_column(self, *, sch:DocTypeCreateSch, created_by:str) -> DocType:
        
        sch.code = await generate_code(entity=CodeCounterEnum.DOC_TYPE)

        db_obj = DocType(**sch.model_dump())

        if created_by:
            db_obj.created_by = db_obj.updated_by = created_by

        db.session.add(db_obj)
        await db.session.flush()

        for obj in sch.doc_archives:
            db_obj_map_archive = DocTypeArchive(doc_format_id=obj.doc_format_id, doc_type_id=db_obj.id, jenis_arsip=obj.jenis_arsip)
            db.session.add(db_obj_map_archive)

        for columns in sch.doc_type_columns:
            db_obj_map_column = DocTypeColumn(doc_type_id=db_obj.id, column_type_id=columns)
            db.session.add(db_obj_map_column)
        
        await db.session.commit()
        await db.session.refresh(db_obj)

        return db_obj

    async def update_and_mapping_w_doc_format_column(self, *, obj_current:DocType, obj_new:DocTypeUpdateSch, updated_by:str) -> DocType:

        obj_data = jsonable_encoder(obj_current)
        update_data = obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])
            elif updated_by and updated_by != "" and field == "updated_by":
                setattr(obj_current, field, updated_by)

        db.session.add(obj_current)
        await db.session.flush()

        current_doc_type_archives = await crud.doc_type_archive.get_by_doc_type(doc_type_id=obj_current.id)

        for dt in obj_new.doc_archives:
            current_doc_type_archive = await crud.doc_type_archive.get_doc_type_archive(doc_type_id=obj_current.id, doc_format_id=dt.doc_format_id, jenis_arsip=dt.jenis_arsip)

            if not current_doc_type_archive:
                doc_format = await crud.doc_format.get(id=dt.doc_format_id)
                if not doc_format:
                    raise HTTPException(status_code=404, detail=f"Document format not found!")

                db_obj_map_archive = DocTypeArchive(doc_format_id=doc_format.id, doc_type_id=obj_current.id, jenis_arsip=dt.jenis_arsip)
                db.session.add(db_obj_map_archive)
            else:
                current_doc_type_archives.remove(current_doc_type_archive)

        current_doc_type_columns = await crud.doc_type_column.get_by_doc_type(doc_type_id=obj_current.id)
        
        for column_type_id in obj_new.doc_type_columns:
            doc_type_column = await crud.doc_type_column.get_doc_type_column(doc_type_id=obj_current.id, column_type_id=column_type_id)
            if not doc_type_column:
                column_type = await crud.column_type.get(id=column_type_id)
                if not column_type:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selected column not found!")
                
                db_obj_map_column = DocTypeColumn(doc_type_id=obj_current.id, column_type_id=column_type_id)
                db.session.add(db_obj_map_column)
                await db.session.flush()
            else:
                current_doc_type_columns.remove(doc_type_column)

        for remove in current_doc_type_archives:
            await db.session.delete(remove)
        
        for current_doc_type_column in current_doc_type_columns:
            await db.session.delete(current_doc_type_column)

        await db.session.commit()
        await db.session.refresh(obj_current)

        return obj_current

    async def get_paginated(self, *, params: Params | None = Params(), login_user: AccessToken | None = None, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs, login_user=login_user)

        return await paginate(db.session, query, params)

    async def get_no_paginated(self, *, login_user: AccessToken | None = None, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs, login_user=login_user)
        response = await db.session.execute(query)

        return response.mappings().all()

    async def get_by_id(self, *, id:str):
        doc_type = await self.fetch_doc_type(id=id)
        if not doc_type: return None
        
        doc_type = DocTypeByIdSch(**doc_type._mapping)
        doc_type.doc_archives = await self.fetch_doc_type_archives(doc_type_id=id)
        doc_type.doc_columns = await self.fetch_doc_type_columns(doc_type_id=id)

        return doc_type

    def base_query(self):

        count_columns_sq = (
            select(func.count(DocType.id).label("jmlh"), DocType.id
                ).join(DocTypeColumn, DocTypeColumn.doc_type_id == DocType.id
                ).group_by(DocType.id).cte("number_of_columns_cte")
        )

        query = select(
                    *DocType.__table__.columns,
                    DocTypeGroup.name.label('doc_type_group_name'),
                    count_columns_sq.c.jmlh.label('number_of_columns')
                )

        query = query.outerjoin(DocTypeGroup, DocTypeGroup.id == DocType.doc_type_group_id
                    ).outerjoin(count_columns_sq, count_columns_sq.c.id == DocType.id
                    ).outerjoin(DepartmentDocType, DepartmentDocType.doc_type_id == DocType.id
                    ).outerjoin(Worker, Worker.department_id == DepartmentDocType.department_id
                    ).outerjoin(DocTypeArchive, DocTypeArchive.doc_type_id == DocType.id)
        
        query = query.distinct()

        return query

    def create_filter(self, *, query, filter:dict, login_user:AccessToken | None = None):
        
        if filter.get("jenis_arsip"):
            query = query.filter(DocTypeArchive.jenis_arsip == filter.get("jenis_arsip"))

        if filter.get("search"):
            search = filter.get("search")
            query = query.filter(
                    or_(
                        cast(DocType.code, String).ilike(f'%{search}%'),
                        cast(DocType.name, String).ilike(f'%{search}%'),
                        cast(DocTypeGroup.name, String).ilike(f'%{search}%')
                    )
                )
            
        if filter.get("order_by"):
            if filter.get("order"):
                order_column = getattr(DocType, filter.get('order_by'), None)
                if order_column is None:
                    raise HTTPException(status_code=400, detail=f'Field {filter.get("order_by")} not found')
                order = filter.get("order")
                if order == OrderEnumSch.descendent:
                    query = query.order_by(order_column.desc())
                if order == OrderEnumSch.ascendent:
                    query = query.order_by(order_column.asc())
            
        if login_user and 'superadmin' not in login_user.authorities:
            query = query.filter(Worker.client_id == login_user.client_id)
        
        return query

    async def fetch_doc_type(self, id:str):
        query = self.base_query()
        query = query.where(DocType.id == id)

        response = await db.session.execute(query)
        return response.one_or_none()
    
    async def fetch_doc_type_archives(self, doc_type_id:str):
        doc_type_archives = await crud.doc_type_archive.fetch_doc_format_by_doc_type(doc_type_id=doc_type_id)
        if not doc_type_archives: return []
        
        document_type_archives = []
        for doc_type_archive in doc_type_archives:
            doc_type_arvh = DocTypeArchiveSch(**doc_type_archive)
            document_type_archives.append(doc_type_arvh)

        return document_type_archives

    async def fetch_doc_type_columns(self, doc_type_id:str):
        doc_type_columns = await crud.doc_type_column.fetch_column_by_doc_type(doc_type_id=doc_type_id)
        if not doc_type_columns: return []

        document_type_columns = []
        for doc_type_column in doc_type_columns:
            doc_type_col = DocTypeColumnSch(**doc_type_column)
            document_type_columns.append(doc_type_col)

        return document_type_columns

doc_type = CRUDDocType(DocType)
