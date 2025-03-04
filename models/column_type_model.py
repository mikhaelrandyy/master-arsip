from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import TipeDataEnum
from typing import TYPE_CHECKING
from models.doc_archive_kolom_model import DocArchiveKolomLink


if TYPE_CHECKING:
    from models import DocType, DocArchive

class ColumnTypeBase(SQLModel):
    name: str | None = Field(nullable=True)
    tipe_data: TipeDataEnum | None = Field(nullable=True)
    enum_data: str | None = Field(nullable=True)
    is_mandatory: bool = Field(nullable=True)
    is_show: bool = Field(nullable=True)
    
class ColumnTypeFullBase(BaseULIDModel, ColumnTypeBase):
    pass

class ColumnType(ColumnTypeFullBase, table=True):
    doc_archives: list["DocArchive"] = Relationship(back_populates="column_types", link_model=DocArchiveKolomLink, sa_relationship_kwargs={"lazy": "select"})

    