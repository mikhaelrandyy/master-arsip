from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field

class DepartementBase(SQLModel):
    code: str | None = Field(nullable=True, unique=True)
    name: str | None = Field(nullable=True)

class DepartementFullBase(BaseULIDModel, DepartementBase):
    pass

class Departement(DepartementFullBase, table=True):
    pass