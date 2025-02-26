from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field
from common.enum import JenisArsipEnum


class DocTypeJenisKolomLinkBase(SQLModel):
    doc_type_id: str = Field(nullable=True, foreign_key='document_type.id', primary_key=True)
    jenis_kolom_id: str = Field(nullable=True, foreign_key='jenis_kolom.id', primary_key=True)
    
class DocTypeJenisKolomLinkFullBase(BaseULIDModel, DocTypeJenisKolomLinkBase):
    pass

class DocTypeJenisKolomLink(DocTypeJenisKolomLinkFullBase, table=True):
    pass