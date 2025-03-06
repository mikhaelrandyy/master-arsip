from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models.doc_type_dept_model import DocTypeDept
from schemas.doc_type_dept_sch import DocTypeDeptCreateSch, DocTypeDeptUpdateSch


class CRUDDocTypeDepartement(CRUDBase[DocTypeDept, DocTypeDeptCreateSch, DocTypeDeptUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocTypeDept:

        query = select(DocTypeDept)
        query = query.where(DocTypeDept.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
doc_type_dept = CRUDDocTypeDepartement(DocTypeDept)
