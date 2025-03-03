from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocTypeArchive
from schemas.doc_format_jenis_arsip_doc_type_link_sch import DocFormatJenisArsipDocTypeCreateSch, DocFormatJenisArsipDocTypeUpdateSch
from common.enum import JenisArsipEnum


class CRUDDocFormatJenisArsipDocType(CRUDBase[DocTypeArchive, DocFormatJenisArsipDocTypeCreateSch,  DocFormatJenisArsipDocTypeUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocTypeArchive:

        query = select(DocTypeArchive)
        query = query.where(DocTypeArchive.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def get_by_doc_type_id(self, *, doc_type_id:str) -> list[DocTypeArchive]:

        query = select(DocTypeArchive)
        query = query.where(DocTypeArchive.doc_type_id == doc_type_id)
        response = await db.session.execute(query)
        return response.scalars().all()

    async def get_by_doc_format_id(self, *, doc_format_id:str, jenis_arsip:JenisArsipEnum) -> DocTypeArchive:

        query = select(DocTypeArchive)
        query = query.where(and_(DocTypeArchive.doc_format_id == doc_format_id,
                                DocTypeArchive.jenis_arsip == jenis_arsip))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def remove(self, *, doc_type_id:str, doc_format_id: str, jenis_arsip:str, db_session: AsyncSession | None = None) -> DocTypeArchive:
        db_session = db_session or db.session

        query = select(DocTypeArchive)
        query = query.where(and_(DocTypeArchive.doc_format_id == doc_format_id,
                                 DocTypeArchive.doc_type_id == doc_type_id,
                                 DocTypeArchive.jenis_arsip == jenis_arsip))

        response = await db_session.execute(query)
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj
     
doc_format_jenis_arsip__doc_type = CRUDDocFormatJenisArsipDocType(DocTypeArchive)
