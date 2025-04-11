from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import DepartmentDocType, DocType, Department, DocTypeGroup
from schemas.department_doc_type_sch import DepartmentDocTypeCreateSch, DepartmentDocTypeUpdateSch


class CRUDDepartmentDocType(CRUDBase[DepartmentDocType, DepartmentDocTypeCreateSch, DepartmentDocTypeUpdateSch]):
    async def get_by_department(self, department_id: str) -> list[DepartmentDocType]:
        query = select(DepartmentDocType)
        query = query.where(DepartmentDocType.department_id == department_id)

        response = await db.session.execute(query)
        return response.scalars().all()
    
    async def get_department_doc_type(self, department_id: str, doc_type_id: str) -> DepartmentDocType:
        query = select(DepartmentDocType)
        query = query.where(and_(DepartmentDocType.department_id == department_id, DepartmentDocType.doc_type_id == doc_type_id))

        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    def base_query(self):

        query = select(
            *DepartmentDocType.__table__.columns,
            Department.name.label('department_name'),
            DocType.name.label('doc_type_name'),
            DocType.code.label('doc_type_code'),
            DocTypeGroup.name.label('doc_type_group_name')
        )
        query = query.join(Department, Department.id == DepartmentDocType.department_id
                    ).join(DocType, DocType.id == DepartmentDocType.doc_type_id
                    ).outerjoin(DocTypeGroup, DocTypeGroup.id == DocType.doc_type_group_id)
        
        query = query.distinct()

        return query
    
    async def fetch_column_by_department(self, department_id: str):
        query = self.base_query()
        query = query.filter(DepartmentDocType.department_id == department_id)
        response = await db.session.execute(query)

        return response.mappings().all()
    
department_doc_type = CRUDDepartmentDocType(DepartmentDocType)
