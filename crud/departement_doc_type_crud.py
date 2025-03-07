from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models.departement_doc_type_model import DepartementDocType
from schemas.departement_doc_type_sch import DepartementDocTypeCreateSch, DepartementDocTypeUpdateSch


class CRUDDepartementDocType(CRUDBase[DepartementDocType, DepartementDocTypeCreateSch, DepartementDocTypeUpdateSch]):
    async def get_by_id(self, *, id:str) -> DepartementDocType:

        query = select(DepartementDocType)
        query = query.where(DepartementDocType.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
departement_doc_type = CRUDDepartementDocType(DepartementDocType)
