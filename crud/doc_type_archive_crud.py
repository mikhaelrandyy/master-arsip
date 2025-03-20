from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocTypeArchive, DocFormat, DocType
from schemas.doc_type_archive_sch import DocTypeArchiveCreateSch, DocTypeArchiveUpdateSch
from common.enum import JenisArsipEnum


class CRUDDocTypeArchive(CRUDBase[DocTypeArchive, DocTypeArchiveCreateSch,  DocTypeArchiveUpdateSch]):
    
    async def get_by_doc_type(self, *, doc_type_id:str) -> list[DocTypeArchive]:

        query = select(DocTypeArchive)
        query = query.where(DocTypeArchive.doc_type_id == doc_type_id)
        response = await db.session.execute(query)
        return response.scalars().all()

    async def get_doc_type_archive(self, *, doc_type_id:str, doc_format_id:str, jenis_arsip:JenisArsipEnum) -> DocTypeArchive:

        query = select(DocTypeArchive)
        query = query.where(and_(
            DocTypeArchive.doc_type_id == doc_type_id,
            DocTypeArchive.doc_format_id == doc_format_id,
            DocTypeArchive.jenis_arsip == jenis_arsip
            )
        )
        response = await db.session.execute(query)
        return response.scalar_one_or_none()

    async def fetch_doc_format_by_doc_type(self, doc_type_id:str):
        query = self.base_query()
        query = query.filter(DocType.id == doc_type_id)
        response = await db.session.execute(query)
        return response.mappings().all()

    def base_query(self):
        query = select(
            *DocTypeArchive.__table__.columns,
            DocFormat.name.label('doc_format_name'),
            DocFormat.code.label('doc_format_code'),
            DocType.name.label('doc_type_name')
        )

        query = query.join(DocFormat, DocFormat.id == DocTypeArchive.doc_format_id
                    ).join(DocType, DocType.id == DocTypeArchive.doc_type_id)
        
        return query

doc_type_archive = CRUDDocTypeArchive(DocTypeArchive)
