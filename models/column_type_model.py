from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import TipeDataEnum
from typing import TYPE_CHECKING
from models.doc_type_column_model import DocTypeColumn
from models.doc_arsip_kolom_model import DocArsipKolomLink


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
    doc_arsips: list["DocArchive"] = Relationship(back_populates="jenis_koloms", link_model=DocArsipKolomLink, sa_relationship_kwargs={"lazy": "select"})

    