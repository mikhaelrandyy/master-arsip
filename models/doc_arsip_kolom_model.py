from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship


class DocArsipKolomLinkBase(SQLModel):
    doc_arsip_id: str | None = Field(nullable=True, foreign_key='document_arsip.id')
    jenis_kolom_id: str | None = Field(nullable=True, foreign_key='jenis_kolom.id')

class DocArsipKolomLinkFullBase(BaseULIDModel, DocArsipKolomLinkBase):
    pass

class DocArsipKolomLink(DocArsipKolomLinkFullBase, table=True):
    pass