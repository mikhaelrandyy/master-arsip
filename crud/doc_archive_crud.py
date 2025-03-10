from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocArchive, DocTypeColumn
from schemas.doc_archive_sch import DocArchiveCreateSch, DocArchiveUpdateSch
from schemas.doc_type_column_sch import DocTypeColumnCreateSch


class CRUDDocArchive(CRUDBase[DocArchive, DocArchiveCreateSch, DocArchiveUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocArchive:

        query = select(DocArchive)
        query = query.where(DocArchive.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create_doc_arsip_and_mapping(self, *, sch:DocArchiveCreateSch, created_by: str | None, db_session: AsyncSession | None = None) -> DocArchive:
        db_session = db_session or db.session

        document_arsip = DocArchive.model_validate(sch.model_dump())

        if created_by:
            document_arsip.created_by = created_by
            document_arsip.updated_by = created_by

        db_session.add(document_arsip)

        await db_session.flush()
        await db_session.refresh(document_arsip)

        for obj in sch.jenis_koloms:

            obj_mapping = DocTypeColumnCreateSch(
                                                doc_type_id=sch.doc_type_id,
                                                column_type_id=obj.id)
                
            obj_mapping_db = DocTypeColumn.model_validate(obj_mapping.model_dump())
            obj_mapping_db.created_by = created_by
            obj_mapping_db.updated_by = created_by
            db_session.add(obj_mapping_db)
            
        await db_session.commit()

        return document_arsip

     
doc_archive = CRUDDocArchive(DocArchive)
