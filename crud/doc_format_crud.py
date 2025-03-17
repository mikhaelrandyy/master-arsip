from fastapi_async_sqlalchemy import db
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import and_, select, or_, cast, String
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocFormat
from schemas.doc_format_sch import DocFormatCreateSch, DocFormatUpdateSch
from common.generator import generate_code
from common.enum import CodeCounterEnum
import crud

class CRUDDocFormat(CRUDBase[DocFormat, DocFormatCreateSch, DocFormatUpdateSch]):
    async def create(self, *, sch:DocFormatCreateSch, created_by:str) -> DocFormat:

        sch.code = await generate_code(entity=CodeCounterEnum.DOC_FORMAT)

        doc_format = DocFormat.model_validate(sch)

        if created_by:
            doc_format.created_by = doc_format.updated_by = created_by

        db.session.add(doc_format)
        await db.session.commit()
        await db.session.refresh(doc_format)

        return doc_format
    
    async def get_paginated(self, *, params: Params, **kwargs):
        query = select(DocFormat)
        query = self.create_filter(query=query, filter=kwargs)

        return await paginate(db.session, query, params)
    
    async def get_no_paginated(self, **kwargs):
        query = select(DocFormat)
        query = self.create_filter(query=query, filter=kwargs)
        return await self.get_all_ordered(query=query)
    
    def create_filter(self, *, query, filter:dict):
        if filter.get("search"):
            search = filter.get("search")
            query = query.filter(
                    or_(
                        cast(DocFormat.code, String).ilike(f'%{search}%'),
                        cast(DocFormat.name, String).ilike(f'%{search}%'),
                        cast(DocFormat.classification, String).ilike(f'%{search}%')
                    )
                )
        return query
        
doc_format = CRUDDocFormat(DocFormat)
