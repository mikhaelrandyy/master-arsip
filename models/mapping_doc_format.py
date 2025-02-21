from sqlmodel import SQLModel, Field


class MappingDocFormat(SQLModel):
    doc_format_id: str = Field(default=None, foreign_key='document_format.id', primary_key=True)
    jenis_arsip_id: str = Field(default=None, foreign_key='jenis_arsip.id', primary_key=True)