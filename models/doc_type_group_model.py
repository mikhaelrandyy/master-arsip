from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocType

class DocTypeGroupBase(SQLModel):
    code: str | None = Field(nullable=True, unique=True)
    name: str | None = Field(nullable=True)

class DocTypeGroupFullBase(BaseULIDModel, DocTypeGroupBase):
    pass

class DocTypeGroup(DocTypeGroupFullBase, table=True):
    document_types: list["DocType"] = Relationship(back_populates="document_type_group", sa_relationship_kwargs = {"lazy": "select"})
