from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import DocumentType
from schemas.document_type_sch import DocumentTypeCreateSch, DocumentTypeUpdateSch


class CRUDDocumentType(CRUDBase[DocumentType, DocumentTypeCreateSch, DocumentTypeUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocumentType:

        query = select(DocumentType)
        query = query.where(DocumentType.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
document_type = CRUDDocumentType(DocumentType)
