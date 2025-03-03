from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import DocTypeGroup
from schemas.document_type_group_sch import DocumentTypeGroupCreateSch, DocumentTypeGroupUpdateSch


class CRUDDocumentTypeGroup(CRUDBase[DocTypeGroup, DocumentTypeGroupCreateSch, DocumentTypeGroupUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocTypeGroup:

        query = select(DocTypeGroup)
        query = query.where(DocTypeGroup.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
document_type_group = CRUDDocumentTypeGroup(DocTypeGroup)
