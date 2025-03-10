from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field

class AlashakBase(SQLModel):
    code: str | None = Field(default=None, nullable=False, unique=True)
    name: str = Field(nullable=False)

class AlashakFullBase(BaseULIDModel, AlashakBase):
    pass

class Alashak(AlashakFullBase, table=True):
    pass