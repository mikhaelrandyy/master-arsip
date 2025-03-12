from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import DocTypeGroup
from schemas.doc_type_group_sch import DocTypeGroupCreateSch, DocTypeGroupUpdateSch
from common.generator import generate_code
from common.enum import CodeCounterEnum


class CRUDDocTypeGroup(CRUDBase[DocTypeGroup, DocTypeGroupCreateSch, DocTypeGroupUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocTypeGroup:

        query = select(DocTypeGroup)
        query = query.where(DocTypeGroup.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
    async def create(self, *, sch:DocTypeGroupCreateSch, created_by:str) -> DocTypeGroup:

        sch.code = await generate_code(entity=CodeCounterEnum.DOC_TYPE_GROUP)

        doc_type_group = DocTypeGroup.model_validate(sch)
        if created_by:
            doc_type_group.created_by = doc_type_group.updated_by = created_by

        db.session.add(doc_type_group)
            
        await db.session.commit()
        await db.session.refresh(doc_type_group)

        return doc_type_group
    
doc_type_group = CRUDDocTypeGroup(DocTypeGroup)
