from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from crud.base_crud import CRUDBase
from models import DocumentType, DocFormatJenisArsipDocTypeLink
from schemas.document_type_sch import DocumentTypeCreateSch, DocumentTypeUpdateSch, DocumentFormatForCreateUpdateDocTypeSch
from schemas.doc_format_jenis_arsip_doc_type_link_sch import DocFormatJenisArsipDocTypeLinkCreateSch
import crud


class CRUDDocumentType(CRUDBase[DocumentType, DocumentTypeCreateSch, DocumentTypeUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocumentType:

        query = select(DocumentType)
        query = query.where(DocumentType.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create_doc_type_and_mapping(self, *, sch:DocumentTypeCreateSch, created_by: str | None, db_session: AsyncSession | None = None) -> DocumentType:
        db_session = db_session or db.session

        document_type = DocumentType.model_validate(sch.model_dump())

        if created_by:
            document_type.created_by = created_by
            document_type.updated_by = created_by

        db_session.add(document_type)

        await db_session.flush()
        await db_session.refresh(document_type)

        for obj in sch.doc_formats:

            obj_mapping = DocFormatJenisArsipDocTypeLinkCreateSch(
                                                                doc_format_id=obj.id,
                                                                doc_type_id=document_type.id,
                                                                jenis_arsip=obj.jenis_arsip)
                
            obj_mapping_db = DocFormatJenisArsipDocTypeLink.model_validate(obj_mapping.model_dump())
            obj_mapping_db.created_by = created_by
            obj_mapping_db.updated_by = created_by
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

        current_doc_type_and_mapping = await crud.doc_format_jenis_arsip__doc_type_link.get_by_doc_type_id(doc_type_id=obj_current.id)
        current_ids = {x.id for x in current_doc_type_and_mapping}

        for dt in obj_new.doc_formats:
            obj_doc_format = await crud.doc_format_jenis_arsip__doc_type_link.get_by_doc_format_id(doc_format_id=dt.id)

            if obj_doc_format is None:
                create_mapping = DocFormatJenisArsipDocTypeLinkCreateSch(doc_format_id=dt.id, doc_type_id=obj_current.id, jenis_arsip=dt.jenis_arsip)
            else:
                current_ids.remove(obj_doc_format.id)

        for remove_id in current_ids:
            await crud.doc_format_jenis_arsip__doc_type_link.remove(id=remove_id)

        return create_mapping

     
document_type = CRUDDocumentType(DocumentType)
