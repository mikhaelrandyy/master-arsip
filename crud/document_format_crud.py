from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import DocumentFormat
from schemas.document_format_sch import DocumentFormatCreateSch, DocumentFormatUpdateSch

class CRUDDocumentFormat(CRUDBase[DocumentFormat, DocumentFormatCreateSch, DocumentFormatUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocumentFormat:

        query = select(DocumentFormat)
        query = query.where(DocumentFormat.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
document_format = CRUDDocumentFormat(DocumentFormat)
