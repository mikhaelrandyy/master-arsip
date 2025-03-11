from crud.base_crud import CRUDBase
from models.unit_model import Unit
from schemas.unit_sch import UnitCreateSch, UnitUpdateSch


class CRUDUnit(CRUDBase[Unit, UnitCreateSch, UnitUpdateSch]):
    pass

unit = CRUDUnit(Unit)
