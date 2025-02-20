from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field

class AlashakBase(SQLModel):
    code: str | None = Field(nullable=True)
    description: str | None = Field(nullable=True)

class AlashakFullBase(BaseULIDModel, AlashakBase):
    pass

class Alashak(AlashakFullBase, table=True):
    pass