from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import DepartementDocType, DocType, Departement
from schemas.departement_doc_type_sch import DepartementDocTypeCreateSch, DepartementDocTypeUpdateSch


class CRUDDepartementDocType(CRUDBase[DepartementDocType, DepartementDocTypeCreateSch, DepartementDocTypeUpdateSch]):
    async def get_by_departement(self, departement_id: str) -> list[DepartementDocType]:
        query = select(DepartementDocType)
        query = query.where(DepartementDocType.departement_id == departement_id)

        response = await db.session.execute(query)
        return response.scalars().all()
    
    async def get_departement_doc_type(self, departement_id: str, doc_type_id: str) -> DepartementDocType:
        query = select(DepartementDocType)
        query = query.where(and_(DepartementDocType.departement_id == departement_id, DepartementDocType.doc_type_id == doc_type_id))

        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    def base_query(self):

        query = select(
            *DepartementDocType.__table__.columns,
            Departement.name.label('departement_name'),
            DocType.name.label('doc_type_name')
        )
        query = query.join(Departement, Departement.id == DepartementDocType.departement_id
                    ).join(DocType, DocType.id == DepartementDocType.doc_type_id)
        
        query = query.distinct()

        return query
    
    async def fetch_column_by_departement(self, departement_id: str):
        query = self.base_query()
        query = query.filter(DepartementDocType.departement_id == departement_id)
        response = await db.session.execute(query)

        return response.mappings().all()
    
departement_doc_type = CRUDDepartementDocType(DepartementDocType)
