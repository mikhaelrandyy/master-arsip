from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocumentFormat
from schemas.document_format_sch import DocumentFormatCreateSch, DocumentFormatUpdateSch

class CRUDDocumentFormat(CRUDBase[DocumentFormat, DocumentFormatCreateSch, DocumentFormatUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocumentFormat:

        query = select(DocumentFormat)
        query = query.where(DocumentFormat.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    # async def create(self, *, sch:DocumentFormatCreateSch, db_session: AsyncSession | None = None) -> DocumentFormat:
    #     db_session = db_session or db.session

    #     doc_format = DocumentFormat.model_validate(sch)

    #     db_session.add(doc_format)
            
    #     await db_session.commit()
    #     await db_session.refresh(doc_format)

    #     return doc_format
        


     
document_format = CRUDDocumentFormat(DocumentFormat)
