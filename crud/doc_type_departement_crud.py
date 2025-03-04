from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models.doc_type_departement_model import DocTypeDepartement
from schemas.doc_type_departement_sch import DocTypeDepartementCreateSch, DocTypeDepartementUpdateSch


class CRUDDocTypeDepartement(CRUDBase[DocTypeDepartement, DocTypeDepartementCreateSch, DocTypeDepartementUpdateSch]):
    async def get_by_id(self, *, id:str) -> DocTypeDepartement:

        query = select(DocTypeDepartement)
        query = query.where(DocTypeDepartement.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
doc_type_departement = CRUDDocTypeDepartement(DocTypeDepartement)
