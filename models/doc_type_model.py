from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from models.doc_type_archive_model import DocTypeArchive
from models.doc_type_column_model import DocTypeColumn

if TYPE_CHECKING:
    from models import DocTypeGroup, DocFormat, Alashak, ColumnType

class DocTypeBase(SQLModel):
    code: str | None = Field(nullable=True, unique=True)
    name: str | None = Field(nullable=True)
    status: bool = Field(nullable=True)
    is_doc_asal: bool = Field(nullable=True)
    is_unit: bool = Field(nullable=True)
    alashak_id: str | None = Field(nullable=True, foreign_key="alashak.id")
    doc_type_group_id: str | None = Field(nullable=True, foreign_key="document_type_group.id")

class DocTypeFullBase(BaseULIDModel, DocTypeBase):
    pass

class DocType(DocTypeFullBase, table=True):
    alashak: "Alashak" = Relationship(sa_relationship_kwargs = {"lazy": "select"})
    document_type_group: "DocTypeGroup" = Relationship(back_populates="document_types", sa_relationship_kwargs = {"lazy": "select"})
    document_formats: list["DocFormat"] = Relationship(link_model=DocTypeArchive, sa_relationship_kwargs = {"lazy": "select", "viewonly":True})
    jenis_koloms: list["ColumnType"] = Relationship(link_model=DocTypeColumn, sa_relationship_kwargs={"lazy": "select", "viewonly":True})

    @property
    def jumlah_jenis_koloms(self) -> int | None:
        return len(self.jenis_koloms)