from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocumentArsip, DoctypeJeniskolom
from schemas.document_arsip_sch import DocumentArsipCreateSch, DocumentArsipUpdateSch
from schemas.doc_type_jenis_kolom_sch import DocTypeJenisKolomCreateSch


class CRUDDocumentArsip(CRUDBase[DocumentArsip, DocumentArsipCreateSch, DocumentArsipUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocumentArsip:

        query = select(DocumentArsip)
        query = query.where(DocumentArsip.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create_doc_arsip_and_mapping(self, *, sch:DocumentArsipCreateSch, created_by: str | None, db_session: AsyncSession | None = None) -> DocumentArsip:
        db_session = db_session or db.session

        document_arsip = DocumentArsip.model_validate(sch.model_dump())

        if created_by:
            document_arsip.created_by = created_by
            document_arsip.updated_by = created_by

        db_session.add(document_arsip)

        await db_session.flush()
        await db_session.refresh(document_arsip)

        for obj in sch.jenis_koloms:

            obj_mapping = DocTypeJenisKolomCreateSch(
                                                        doc_type_id=sch.doc_type_id,
                                                        jenis_kolom_id=obj.id)
                
            obj_mapping_db = DoctypeJeniskolom.model_validate(obj_mapping.model_dump())
            obj_mapping_db.created_by = created_by
            obj_mapping_db.updated_by = created_by
            db_session.add(obj_mapping_db)
            
        await db_session.commit()

        return document_arsip

     
document_arsip = CRUDDocumentArsip(DocumentArsip)
