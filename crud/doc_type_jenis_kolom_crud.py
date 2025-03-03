from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocTypeColumn
from schemas.document_type_sch import DocumentTypeSch
from schemas.doc_type_jenis_kolom_sch import DocTypeJenisKolomSch, DocTypeJenisKolomCreateSch, DocTypeJenisKolomUpdateSch, DocTypeJenisKolomForMappingSch
from schemas.jenis_kolom_sch import jenisKolomByIdForMappingSch
import crud


class CRUDMappingDocTypeJenisKolomLink(CRUDBase[DocTypeJenisKolomSch, DocTypeJenisKolomCreateSch, DocTypeJenisKolomUpdateSch]):
    async def get_by_doc_type_id(self, *, doc_type_id:str) -> list[DocTypeColumn]:

        query = select(DocTypeColumn)
        query = query.where(DocTypeColumn.doc_type_id == doc_type_id)
        response = await db.session.execute(query)
        return response.scalars().all()

    async def get_by_doc_type_jenis_kolom(self, *, doc_type_id: str, jenis_kolom_id:str) -> DocTypeColumn:

        query = select(DocTypeColumn)
        query = query.where(and_(DocTypeColumn.doc_type_id == doc_type_id,
                                 DocTypeColumn.jenis_kolom_id == jenis_kolom_id))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create_mapping_doc_type_jenis_kolom(self, *, sch: DocTypeJenisKolomForMappingSch, db_session: AsyncSession | None = None):
        db_session = db_session or db.session

        for jns in sch.jenis_koloms:
            mapping_db = DocTypeColumn(doc_type_id=sch.doc_type_id, jenis_kolom_id=jns)
            db_session.add(mapping_db) 

        await db_session.commit()

        return sch.doc_type_id
    
    async def update_mapping_doc_type_jenis_kolom(self, *, obj_new:DocTypeJenisKolomUpdateSch, db_session: AsyncSession | None = None) -> DocTypeColumn:
        db_session = db_session or db.session

        # obj_current = await crud.doc_type_jenis_kolom.get_by_doc_type_id(doc_type_id=obj_new.doc_type_id)

        # if not obj_current:
        #     raise HTTPException(status_code=404, detail=f"Document Type tidak ditemukan")
        
        # for doc in obj_current:
        
        current_doctype_jeniskolom = await crud.doc_type_jenis_kolom.get_by_doc_type_id(doc_type_id=obj_new.doc_type_id)

        for dt in obj_new.jenis_koloms:
            obj_jns_kolom = await crud.doc_type_jenis_kolom.get_by_doc_type_jenis_kolom(doc_type_id=obj_new.doc_type_id, jenis_kolom_id=dt)

            if obj_jns_kolom is None:
                jns_kolom = await crud.jenis_kolom.get(id=dt)

                if not jns_kolom:
                    raise HTTPException(status_code=404, detail=f"Jenis Kolom tidak tersedia")
                
                mapping_db = DocTypeColumn(doc_type_id=obj_new.doc_type_id, jenis_kolom_id=dt)
                db_session.add(mapping_db)
            else:
                current_doctype_jeniskolom.remove(obj_jns_kolom)

        for remove in current_doctype_jeniskolom:
            await crud.doc_type_jenis_kolom.remove(doc_type_id=remove.doc_type_id, jenis_kolom_id=remove.jenis_kolom_id)

        await db_session.commit()

        return obj_new.doc_type_id
    
    async def remove(self, *, doc_type_id:str, jenis_kolom_id: str, db_session: AsyncSession | None = None) -> DocTypeColumn:
        db_session = db_session or db.session

        query = select(DocTypeColumn)
        query = query.where(and_(DocTypeColumn.doc_type_id == doc_type_id,
                                 DocTypeColumn.jenis_kolom_id == jenis_kolom_id))

        response = await db_session.execute(query)
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj


doc_type_jenis_kolom = CRUDMappingDocTypeJenisKolomLink(DocTypeColumn)
