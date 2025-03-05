from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from crud.base_crud import CRUDBase
from models import DocType, DocTypeArchive, DocFormat
from schemas.doc_type_sch import DocTypeCreateSch, DocTypeUpdateSch
from schemas.doc_type_archive_sch import DocTypeArchiveCreateSch
from common.generator import generate_code
from common.enum import CodeCounterEnum
import crud


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

     
doc_type = CRUDDocType(DocType)
