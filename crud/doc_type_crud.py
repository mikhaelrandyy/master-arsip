from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params, Page
from sqlmodel import and_, select, cast, String, or_, func
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from crud.base_crud import CRUDBase
from models import DocType, DocTypeArchive, DocTypeGroup, DepartementDocType, Worker, DocTypeColumn
from schemas.doc_type_sch import DocTypeCreateSch, DocTypeUpdateSch
from schemas.doc_type_archive_sch import DocTypeArchiveCreateSch
from common.generator import generate_code
from common.enum import CodeCounterEnum
import crud
import json

class CRUDDocType(CRUDBase[DocType, DocTypeCreateSch, DocTypeUpdateSch]):

    async def get_by_id(self, *, id:str) -> DocType:

        query = select(DocType)
        query = query.where(DocType.id == id)
        query = query.options(selectinload(DocType.doc_type_group)
                    ).options(selectinload(DocType.column_types)
                    ).options(selectinload(DocType.doc_formats))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create_and_mapping(self, *, sch:DocTypeCreateSch, created_by:str, db_session: AsyncSession | None = None) -> DocType:
        db_session = db_session or db.session

        sch.code = await generate_code(entity=CodeCounterEnum.DOC_TYPE, db_session=db_session)

        db_obj = DocType.model_validate(sch)

        if created_by:
            db_obj.created_by = db_obj.updated_by = created_by

        db_session.add(db_obj)
        await db_session.flush()
        await db_session.refresh(db_obj)

        for obj in sch.doc_archives:
            db_obj_mapping = DocTypeArchive(doc_format_id=obj.id, doc_type_id=db_obj.id, jenis_arsip=obj.jenis_arsip)
            db_session.add(db_obj_mapping)
            
        await db_session.commit()

        return db_obj

    async def update_doc_type_and_mapping(self, *, obj_current:DocType, obj_new:DocTypeUpdateSch, updated_by:str, db_session: AsyncSession | None = None) -> DocType:
        db_session = db_session or db.session

        obj_data = jsonable_encoder(obj_current)
        update_data = obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])
            elif updated_by and updated_by != "" and field == "updated_by":
                setattr(obj_current, field, updated_by)

        db_session.add(obj_current)
        await db_session.flush()

        current_doc_type_archives = await crud.doc_type_archive.get_by_doc_type_id(doc_type_id=obj_current.id)

        for dt in obj_new.doc_archives:
            current_doc_type_archive = await crud.doc_type_archive.get_doc_type_archive(doc_type_id=obj_current.id, doc_format_id=dt.id, jenis_arsip=dt.jenis_arsip)

            if not current_doc_type_archive:
                doc_format = await crud.doc_format.get(id=dt.id)
                if not doc_format:
                    raise HTTPException(status_code=404, detail=f"Document format not found!")

                db_obj_mapping = DocTypeArchive(doc_format_id=dt.id, doc_type_id=obj_current.id, jenis_arsip=dt.jenis_arsip)
                db_session.add(db_obj_mapping)
            else:
                current_doc_type_archives.remove(current_doc_type_archive)

        for remove in current_doc_type_archives:
            await crud.doc_type_archive.remove(doc_type_id=remove.doc_type_id, doc_format_id=remove.doc_format_id, jenis_arsip=remove.jenis_arsip)

        await db_session.commit()
        await db_session.refresh(obj_current)

        return obj_current

    async def get_paginated(self, params, login_user, db_session: AsyncSession | None = None, **kwargs):
        db_session = db_session or db.session

        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs, login_user=login_user)

        return await paginate(db_session, query, params)

    def base_query(self):

        columns_sq = (
            select(func.count(DocType.id).label("jmlh"), DocType.id
                ).join(DocTypeColumn, DocTypeColumn.doc_type_id == DocType.id
                ).group_by(DocType.id).cte("number_of_columns_cte")
        )

        query = select(
                    *DocType.__table__.columns,
                    DocTypeGroup.name.label('doc_type_group_name'),
                    columns_sq.c.jmlh.label('number_of_columns')
                )

        query = query.outerjoin(DocTypeGroup, DocTypeGroup.id == DocType.doc_type_group_id
                    ).outerjoin(columns_sq, columns_sq.c.id == DocType.id)
                    
        query = query.join(DepartementDocType, DepartementDocType.doc_type_id == DocType.id
                    ).join(Worker, Worker.dept_id == DepartementDocType.dept_id)

        return query

    def create_filter(self, query, filter:dict, login_user):

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
            order_column = getattr(DocType, filter.get('order_by'))
            query = query.order_by(order_column.desc())

        if login_user and 'superadmin' not in login_user.authorities:
            query = query.filter(Worker.client_id == login_user.client_id)
        
        return query


doc_type = CRUDDocType(DocType)
