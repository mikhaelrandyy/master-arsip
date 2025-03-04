from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import Departement, DocTypeDepartement
from schemas.departement_sch import DepartementCreateSch, DepartementUpdateSch, DepartementCreateForMappingSch
from schemas.doc_type_departement_sch import DocTypeDepartementCreateSch

class CRUDDepartement(CRUDBase[Departement, DepartementCreateSch, DepartementUpdateSch]):
   async def get_by_id(self, *, id:str) -> Departement:

        query = select(Departement)
        query = query.where(Departement.id == id)
        query = query.options(selectinload(Departement.doc_types))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
   
   async def create_departement_mapping(self, *, sch:DepartementCreateForMappingSch, created_by:str, db_session: AsyncSession | None = None) -> Departement:
      db_session = db_session or db.session

      departement = Departement.model_validate(sch)

      if created_by:
         departement.created_by = departement.updated_by = created_by

      await db_session.flush()
      db_session.add(departement)
         
      for dt in sch.doc_types:
         mapping_obj = DocTypeDepartementCreateSch(doc_type_id=dt.id, departement_id=departement.id)
         obj_mapping_db = DocTypeDepartement.model_validate(mapping_obj.model_dump())
         db_session.add(obj_mapping_db)
      
      await db_session.commit()

      return departement
     
departement = CRUDDepartement(Departement)
