# from models.base_model import BaseULIDModel
# from sqlmodel import SQLModel, Field, Relationship


# class DocArchiveColumnBase(SQLModel):
#     doc_archive_id: str | None = Field(nullable=True, foreign_key='doc_archive.id')
#     column_type_id: str | None = Field(nullable=True, foreign_key='column_type.id')

# class DocArchiveColumnFullBase(BaseULIDModel, DocArchiveColumnBase):
#     pass

# class DocArchiveColumn(DocArchiveColumnFullBase, table=True):
#     pass