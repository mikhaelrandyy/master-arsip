from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from crud.base_crud import CRUDBase
from models import DocumentType, DocformatJenisarsipDoctype, DocumentFormat
from schemas.document_type_sch import DocumentTypeCreateSch, DocumentTypeUpdateSch
from schemas.doc_format_jenis_arsip_doc_type_link_sch import DocFormatJenisArsipDocTypeCreateSch
from common.generator import generate_code
import crud


class CRUDDocumentType(CRUDBase[DocumentType, DocumentTypeCreateSch, DocumentTypeUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocumentType:

        query = select(DocumentType)
        query = query.where(DocumentType.id == id)
        query = query.options(selectinload(DocumentType.jenis_koloms), selectinload(DocumentType.document_formats
                    ).options(joinedload(DocumentFormat.doc_format_link)))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create_doc_type_and_mapping(self, *, sch:DocumentTypeCreateSch, created_by:str, db_session: AsyncSession | None = None) -> DocumentType:
        db_session = db_session or db.session

        sch.code = generate_code(format_code="CJD")
        document_type = DocumentType.model_validate(sch.model_dump())

        if created_by:
            document_type.created_by = created_by
            document_type.updated_by = created_by

        db_session.add(document_type)

        await db_session.flush()
        await db_session.refresh(document_type)

        for obj in sch.document_formats:

            obj_mapping = DocFormatJenisArsipDocTypeCreateSch(
                                                                doc_format_id=obj.id,
                                                                doc_type_id=document_type.id,
                                                                jenis_arsip=obj.jenis_arsip)
                
            obj_mapping_db = DocformatJenisarsipDoctype.model_validate(obj_mapping.model_dump())
            db_session.add(obj_mapping_db)
            
        await db_session.commit()

        return document_type

    async def update_doc_type_and_mapping(self, *, obj_current:DocumentType, obj_new:DocumentTypeUpdateSch, updated_by:str, db_session: AsyncSession | None = None) -> DocumentType:
        db_session = db_session or db.session

        obj_data = jsonable_encoder(obj_current)
        update_data = obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])
            elif updated_by and updated_by != "" and field == "updated_by":
                setattr(obj_current, field, updated_by)

        current_doc_type_and_mapping = await crud.doc_format_jenis_arsip__doc_type.get_by_doc_type_id(doc_type_id=obj_current.id)

        for dt in obj_new.document_formats:
            obj_doc_format = await crud.doc_format_jenis_arsip__doc_type.get_by_doc_format_id(doc_format_id=dt.id, jenis_arsip=dt.jenis_arsip)

            if obj_doc_format is None:

                doc_format = await crud.document_format.get_by_id(id=dt.id)

                if not doc_format:
                    raise HTTPException(status_code=404, detail=f"Document Format tidak tersedia")

                mapping_db = DocformatJenisarsipDoctype(doc_format_id=dt.id, doc_type_id=obj_current.id, jenis_arsip=dt.jenis_arsip)
                db_session.add(mapping_db)
            else:
                current_doc_type_and_mapping.remove(obj_doc_format)

        for remove in current_doc_type_and_mapping:
            await crud.doc_format_jenis_arsip__doc_type.remove(doc_type_id=remove.doc_type_id, doc_format_id=remove.doc_format_id, jenis_arsip=remove.jenis_arsip)

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)

        return obj_current

     
document_type = CRUDDocumentType(DocumentType)
