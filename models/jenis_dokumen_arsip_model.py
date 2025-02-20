from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field

class JenisDokumenArsipBase(SQLModel):
    name: str | None = Field(nullable=True)

class JenisDokumenArsipFullBase(BaseULIDModel, JenisDokumenArsipBase):
    pass

class JenisDokumenArsip(JenisDokumenArsipFullBase, table=True):
    pass