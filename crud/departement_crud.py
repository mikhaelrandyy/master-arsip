from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import Departement, DepartementDocType
from schemas.departement_sch import DepartementCreateSch, DepartementUpdateSch, DepartementCreateForMappingSch, DepartementSch
from schemas.departement_doc_type_sch import DepartementDocTypeCreateSch
import crud

class CRUDDepartement(CRUDBase[Departement, DepartementCreateSch, DepartementUpdateSch]):
   async def get_by_id(self, *, id:str) -> Departement:

        query = select(Departement)
        query = query.where(Departement.id == id)
        query = query.options(selectinload(Departement.doc_types))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
   
   async def create_dept_mapping(self, *, sch:DepartementCreateForMappingSch, db_session: AsyncSession | None = None) -> DepartementSch:
      db_session = db_session or db.session

      jumlah_doc_type = len(sch.doc_types)

      obj_dept = await crud.departement.get_by_id(id=sch.id)
      
      for dt in sch.doc_types:
         mapping_obj = DepartementDocType(doc_type_id=dt.id, dept_id=sch.id)
         db_session.add(mapping_obj)
      
      response_obj = DepartementSch(code=obj_dept.code, name=obj_dept.name, jumlah_doc_type=jumlah_doc_type)

      await db_session.commit()

      return response_obj
     
departement = CRUDDepartement(Departement)
