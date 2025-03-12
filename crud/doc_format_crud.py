from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocFormat
from schemas.doc_format_sch import DocFormatCreateSch, DocFormatUpdateSch
from common.generator import generate_code
from common.enum import CodeCounterEnum
import crud

class CRUDDocFormat(CRUDBase[DocFormat, DocFormatCreateSch, DocFormatUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocFormat:

        query = select(DocFormat)
        query = query.where(DocFormat.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create(self, *, sch:DocFormatCreateSch, created_by:str) -> DocFormat:

        sch.code = await generate_code(entity=CodeCounterEnum.DOC_FORMAT)

        doc_format = DocFormat.model_validate(sch)

        if created_by:
            doc_format.created_by = doc_format.updated_by = created_by

        db.session.add(doc_format)
        await db.session.commit()
        await db.session.refresh(doc_format)

        return doc_format
        
doc_format = CRUDDocFormat(DocFormat)
