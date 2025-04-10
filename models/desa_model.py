from sqlmodel import SQLModel, Field
from models.base_model import BaseULIDModel

class DesaBase(SQLModel):
    code: str = Field(nullable=True, unique=True)
    name: str = Field(nullable=True, unique=True)

class DesaFullBase(DesaBase, BaseULIDModel):
    pass

class Desa(DesaFullBase, table=True):
    pass