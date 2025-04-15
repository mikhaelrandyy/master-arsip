from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from pydantic import field_validator

if TYPE_CHECKING:
    from models import DocType

class DocTypeGroupBase(SQLModel):
    code: str | None = Field(nullable=False, default=None, unique=True)
    name: str | None = Field(nullable=False)

    @field_validator('name')
    def validate_name(cls, value):
        return value.strip()

class DocTypeGroupFullBase(BaseULIDModel, DocTypeGroupBase):
    pass

class DocTypeGroup(DocTypeGroupFullBase, table=True):
    pass
