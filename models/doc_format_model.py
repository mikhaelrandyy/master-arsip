from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from common.enum import DocumentClassificationEnum
from typing import TYPE_CHECKING
from models.doc_type_archive_model import DocTypeArchive
from pydantic import field_validator

if TYPE_CHECKING:
    from models import DocType

class DocFormatBase(SQLModel):
    code: str | None = Field(nullable=False, default=None, unique=True)
    name: str | None = Field(nullable=True)
    classification: DocumentClassificationEnum | None = Field(nullable=True)

    @field_validator('name')
    def validate_name(cls, value):
        return value.strip()

class DocFormatFullBase(BaseULIDModel, DocFormatBase):
    pass

class DocFormat(DocFormatFullBase, table=True):
    doc_format_link: "DocTypeArchive" = Relationship(sa_relationship_kwargs = {"lazy": "select"})

    @property
    def jenis_arsip(self) -> str | None:
        return getattr(getattr(self, "doc_format_link", None), "jenis_arsip", None)