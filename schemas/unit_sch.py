from models.unit_model import UnitBase, UnitFullBase
from sqlmodel import SQLModel

class UnitCreateSch(UnitBase):
    pass

class UnitSch(UnitFullBase):
    pass

class UnitUpdateSch(UnitBase):
    pass

class UnitByIdSch(UnitFullBase):
    pass
