from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from models.doc_type_archive_model import DocTypeArchive
from models.doc_type_column_model import DocTypeColumn
from models.departement_doc_type_model import DepartementDocType

if TYPE_CHECKING:
    from models import DocTypeGroup, DocFormat, Alashak, ColumnType, Departement

class DocTypeBase(SQLModel):
    code: str | None = Field(nullable=True, unique=True)
    name: str | None = Field(nullable=True)
    status: bool = Field(nullable=True)
    is_doc_asal: bool = Field(nullable=True)
    is_unit: bool = Field(nullable=True)
    alashak_id: str | None = Field(nullable=True, foreign_key="alashak.id")
    doc_type_group_id: str | None = Field(nullable=True, foreign_key="doc_type_group.id")

class DocTypeFullBase(BaseULIDModel, DocTypeBase):
    pass

class DocType(DocTypeFullBase, table=True):
    departement: "Departement" = Relationship(back_populates="doc_types", link_model=DepartementDocType, sa_relationship_kwargs = {"lazy": "select"})
    alashak: "Alashak" = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    doc_type_group: "DocTypeGroup" = Relationship(back_populates="doc_types", sa_relationship_kwargs = {"lazy": "select"})
    doc_formats: list["DocFormat"] = Relationship(link_model=DocTypeArchive, sa_relationship_kwargs = {"lazy": "select", "viewonly":True})
    column_types: list["ColumnType"] = Relationship(link_model=DocTypeColumn, sa_relationship_kwargs={"lazy": "select", "viewonly":True})

    @property
    def jumlah_colum_type(self) -> int | None:
        return len(self.column_types)
    
    @property
    def doc_type_group_name(self) -> str | None:
        return getattr(getattr(self, 'document_type_group', None), 'name', None)