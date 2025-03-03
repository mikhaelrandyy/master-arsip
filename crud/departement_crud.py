from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import Departement
from schemas.departement_sch import DepartementCreateSch, DepartementUpdateSch

class CRUDDepartement(CRUDBase[Departement, DepartementCreateSch, DepartementUpdateSch]):
    pass
     
departement = CRUDDepartement(Departement)
