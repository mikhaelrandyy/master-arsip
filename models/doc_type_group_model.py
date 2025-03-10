from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocType

class DocTypeGroupBase(SQLModel):
    code: str | None = Field(nullable=False, default=None, unique=True)
    name: str | None = Field(nullable=False)

class DocTypeGroupFullBase(BaseULIDModel, DocTypeGroupBase):
    pass

class DocTypeGroup(DocTypeGroupFullBase, table=True):
    pass
