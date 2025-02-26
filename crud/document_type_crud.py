from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocumentType, DocFormatJenisArsipDocTypeLink
from schemas.document_type_sch import DocumentTypeCreateSch, DocumentTypeUpdateSch
from schemas.doc_format_jenis_arsip_doc_type_link_sch import DocFormatJenisArsipDocTypeLinkCreateSch


class CRUDDocumentType(CRUDBase[DocumentType, DocumentTypeCreateSch, DocumentTypeUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocumentType:

        query = select(DocumentType)
        query = query.where(DocumentType.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create(self, *, sch:DocumentTypeCreateSch, db_session: AsyncSession | None = None) -> DocumentType:
        db_session = db_session or db.session

        document_type = DocumentType.model_validate(sch.model_dump())
        db_session.add(document_type)

        await db_session.flush()
        await db_session.refresh(document_type)

        for obj in sch.doc_formats:

            obj_mapping = DocFormatJenisArsipDocTypeLinkCreateSch(doc_format_id=obj.id,
                                                                      doc_type_id=document_type.id,
                                                                      jenis_arsip=obj.jenis_arsip)
                
            obj_mapping_db = DocFormatJenisArsipDocTypeLink.model_validate(obj_mapping.model_dump())
            db_session.add(obj_mapping_db)
            
        await db_session.commit()

        return document_type

     
document_type = CRUDDocumentType(DocumentType)
