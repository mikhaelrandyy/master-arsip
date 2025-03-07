from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params, Page
from sqlmodel import and_, select, cast, String, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from crud.base_crud import CRUDBase
from models import DocType, DocTypeArchive, DocTypeGroup, DepartementDocType, Worker
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
    
    async def create_doc_type_and_mapping(self, *, sch:DocTypeCreateSch, created_by:str, db_session: AsyncSession | None = None) -> DocType:
        db_session = db_session or db.session

        sch.code = await generate_code(entity=CodeCounterEnum.DOC_TYPE, db_session=db_session)

        document_type = DocType.model_validate(sch)

        if created_by:
            document_type.created_by = created_by
            document_type.updated_by = created_by

        db_session.add(document_type)

        await db_session.flush()
        await db_session.refresh(document_type)

        for obj in sch.document_formats:

            obj_mapping = DocTypeArchiveCreateSch(
                                                doc_format_id=obj.id,
                                                doc_type_id=document_type.id,
                                                jenis_arsip=obj.jenis_arsip)
                
            obj_mapping_db = DocTypeArchive.model_validate(obj_mapping.model_dump())
            db_session.add(obj_mapping_db)
            
        await db_session.commit()

        return document_type

    async def update_doc_type_and_mapping(self, *, obj_current:DocType, obj_new:DocTypeUpdateSch, updated_by:str, db_session: AsyncSession | None = None) -> DocType:
        db_session = db_session or db.session

        obj_data = jsonable_encoder(obj_current)
        update_data = obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])
            elif updated_by and updated_by != "" and field == "updated_by":
                setattr(obj_current, field, updated_by)

        current_doc_type_and_mapping = await crud.doc_type_archive.get_by_doc_type_id(doc_type_id=obj_current.id)

        for dt in obj_new.document_formats:
            obj_doc_format = await crud.doc_type_archive.get_by_doc_format_id(doc_format_id=dt.id, jenis_arsip=dt.jenis_arsip)

            if obj_doc_format is None:

                doc_format = await crud.doc_format.get_by_id(id=dt.id)

                if not doc_format:
                    raise HTTPException(status_code=404, detail=f"Document Format tidak tersedia")

                mapping_db = DocTypeArchive(doc_format_id=dt.id, doc_type_id=obj_current.id, jenis_arsip=dt.jenis_arsip)
                db_session.add(mapping_db)
            else:
                current_doc_type_and_mapping.remove(obj_doc_format)

        for remove in current_doc_type_and_mapping:
            await crud.doc_type_archive.remove(doc_type_id=remove.doc_type_id, doc_format_id=remove.doc_format_id, jenis_arsip=remove.jenis_arsip)

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)

        return obj_current

    async def get_paginated(self, params, login_info, db_session: AsyncSession | None = None, **kwargs):
        db_session = db_session or db.session

        query = self.base_query()

        query = self.create_filter(query=query, filter=kwargs, login_info=login_info)

        return await paginate(db_session, query, params)

    def base_query(self):
        query = select(DocType).outerjoin(DocTypeGroup, DocTypeGroup.id == DocType.doc_type_group_id
                            ).outerjoin(DepartementDocType, DepartementDocType.doc_type_id == DocType.id
                            ).outerjoin(Worker, Worker.departement_id == DepartementDocType.dept_id)

        return query

    def create_filter(self, query, filter:dict, login_info):

        authorities = login_info.authorities
        search = filter.get("search")
        order_by = filter.get("order_by") 

        if "superadmin" in authorities:
            return query
        
        if login_info:
            query = query.filter(Worker.client_id == login_info.client_id)

        if search:
            query = query.filter(
                    or_(
                        cast(DocType.code, String).ilike(f'%{search}%'),
                        cast(DocType.name, String).ilike(f'%{search}%'),
                        cast(DocTypeGroup.name, String).ilike(f'%{search}%')
                    )
                )
            
        if order_by:
            query = query.order_by(order_by)
        
        return query


doc_type = CRUDDocType(DocType)
