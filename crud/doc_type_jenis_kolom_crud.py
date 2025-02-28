from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DoctypeJeniskolom
from schemas.doc_type_jenis_kolom_sch import DocTypeJenisKolomSch, DocTypeJenisKolomCreateSch, DocTypeJenisKolomUpdateSch, DocTypeJenisKolomForMappingSch, DocTypeJenisKolomMappingSch
import crud


class CRUDMappingDocTypeJenisKolomLink(CRUDBase[DocTypeJenisKolomSch, DocTypeJenisKolomCreateSch, DocTypeJenisKolomUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocTypeJenisKolomSch:

        query = select(DoctypeJeniskolom)
        query = query.where(DoctypeJeniskolom.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create_mapping_doc_type_jenis_kolom(self, *, sch: DocTypeJenisKolomForMappingSch, created_by: str | None, db_session: AsyncSession | None = None) -> list[DocTypeJenisKolomMappingSch]:
        db_session = db_session or db.session

        jumlah_jenis_kolom = len(sch.jenis_koloms)
        new_documents: list[DocTypeJenisKolomCreateSch] = []
        doc_arsips: list[DocTypeJenisKolomMappingSch] = []

        for jns in sch.jenis_koloms:
            mapping_db = DoctypeJeniskolom(doc_type_id=sch.doc_type_id, jenis_kolom_id=jns)
            db_session.add(mapping_db) 
            new_documents.append(mapping_db)

        await db_session.flush()

        for x in new_documents:
            obj_doc_type = await crud.document_type.get(id=x.doc_type_id)
            obj_mapping = DocTypeJenisKolomMappingSch(document_type_name=obj_doc_type.name, doc_type_id=obj_doc_type.id, jumlah_jenis_kolom=jumlah_jenis_kolom)
            doc_arsips.append(obj_mapping)

        await db_session.commit()

        return doc_arsips

doc_type_jenis_kolom = CRUDMappingDocTypeJenisKolomLink(DoctypeJeniskolom)
