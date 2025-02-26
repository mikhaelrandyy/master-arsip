from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import DocTypeJenisKolomLink
from schemas.doc_type_jenis_kolom_sch import DocTypeJenisKolomLinkCreateSch, DocTypeJenisKolomLinkUpdateSch


class CRUDDocTypeJenisKolomLink(CRUDBase[DocTypeJenisKolomLink, DocTypeJenisKolomLinkCreateSch,  DocTypeJenisKolomLinkUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocTypeJenisKolomLink:

        query = select(DocTypeJenisKolomLink)
        query = query.where(DocTypeJenisKolomLink.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
doc_type_jenis_kolom_link = CRUDDocTypeJenisKolomLink(DocTypeJenisKolomLink)
