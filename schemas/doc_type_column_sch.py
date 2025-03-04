from models.doc_type_column_model import DocTypeColumnBase
from models.base_model import SQLModel


class DocTypeColumnCreateSch(DocTypeColumnBase):
    pass

class DocTypeColumnSch(DocTypeColumnBase):
    pass

class DocTypeColumnUpdateSch(DocTypeColumnBase):
    pass

class DocTypeColumnByIdSch(DocTypeColumnBase):
    pass

class DocTypeColumnCreateUpdateSch(SQLModel):
    doc_type_id: str | None
    column_types: list[str] | None
