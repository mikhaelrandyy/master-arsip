from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import DocFormatJenisArsipDocTypeLink
from schemas.doc_format_jenis_arsip_doc_type_link_sch import DocFormatJenisArsipDocTypeLinkCreateSch, DocFormatJenisArsipDocTypeLinkUpdateSch


class CRUDDocFormatJenisArsipDocTypeLink(CRUDBase[DocFormatJenisArsipDocTypeLink, DocFormatJenisArsipDocTypeLinkCreateSch,  DocFormatJenisArsipDocTypeLinkUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocFormatJenisArsipDocTypeLink:

        query = select(DocFormatJenisArsipDocTypeLink)
        query = query.where(DocFormatJenisArsipDocTypeLink.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
doc_format_jenis_arsip__doc_type_link = CRUDDocFormatJenisArsipDocTypeLink(DocFormatJenisArsipDocTypeLink)
