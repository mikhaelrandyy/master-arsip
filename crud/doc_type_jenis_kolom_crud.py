from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocTypeJenisKolomLink
from schemas.doc_type_jenis_kolom_link_sch import DocTypeJenisKolomLinkSch, DocTypeJenisKolomLinkCreateSch, DocTypeJenisKolomLinkUpdateSch, DocTypeJenisKolomLinkForMappingSch
from schemas.jenis_kolom_sch import JenisKolomCreateSch



class CRUDMappingDocTypeJenisKolomLink(CRUDBase[DocTypeJenisKolomLinkSch, DocTypeJenisKolomLinkCreateSch, DocTypeJenisKolomLinkUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocTypeJenisKolomLinkSch:

        query = select(DocTypeJenisKolomLink)
        query = query.where(DocTypeJenisKolomLink.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create_mapping(self, *, sch: DocTypeJenisKolomLinkForMappingSch, created_by: str | None, db_session: AsyncSession | None = None) -> DocTypeJenisKolomLinkForMappingSch:
        db_session = db_session or db.session
        
        new_documents: list[DocTypeJenisKolomLinkCreateSch] = []

        for jns in sch.jenis_koloms:
            obj_in = DocTypeJenisKolomLinkCreateSch(doc_type_id=sch.doc_type_id, jenis_kolom_id=jns)
            new_documents.append(obj_in)
            mapping_db = DocTypeJenisKolomLink.model_validate(obj_in)

            if created_by:
                mapping_db.created_by = mapping_db.updated_by = created_by
                
            db_session.add(mapping_db) 

        obj_mapping = DocTypeJenisKolomLinkForMappingSch(doc_type_id=sch.doc_type_id, jenis_koloms=[jns for jns in sch.jenis_koloms])

        await db_session.commit()

        return obj_mapping

doc_type_jenis_kolom_link = CRUDMappingDocTypeJenisKolomLink(DocTypeJenisKolomLink)
