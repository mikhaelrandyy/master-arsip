from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from models.doc_type_archive_model import DocTypeArchive
from models.doc_type_column_model import DocTypeColumn

if TYPE_CHECKING:
    from models import DocTypeGroup, DocFormat, ColumnType

class DocTypeBase(SQLModel):
    code: str | None = Field(nullable=True, default=None, unique=True)
    name: str | None = Field(nullable=True)
    doc_type_group_id: str | None = Field(nullable=True, foreign_key="doc_type_group.id")
    is_doc_asal: bool = Field(nullable=False, default=False)
    is_multiple: bool = Field(nullable=False, default=False)
    is_active: bool = Field(nullable=False, default=True)

class DocTypeFullBase(BaseULIDModel, DocTypeBase):
    pass

class DocType(DocTypeFullBase, table=True):
    doc_formats: list["DocFormat"] = Relationship(link_model=DocTypeArchive, sa_relationship_kwargs = {"lazy": "select", "viewonly":True})
    column_types: list["ColumnType"] = Relationship(link_model=DocTypeColumn, sa_relationship_kwargs={"lazy": "select", "viewonly":True})
    doc_type_group: "DocTypeGroup" = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    
    