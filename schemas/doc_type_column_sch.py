from models.doc_type_column_model import DocTypeColumnBase
from models.base_model import SQLModel
from common.enum import DataTypeEnum


class DocTypeColumnCreateSch(DocTypeColumnBase):
    pass

class DocTypeColumnSch(DocTypeColumnBase):
    column_name: str | None = None
    column_is_mandatory: bool | None = None
    column_data_type: DataTypeEnum | None = None
    column_enum_data: str | None = None


class DocTypeColumnUpdateSch(DocTypeColumnBase):
    pass

class DocTypeColumnByIdSch(DocTypeColumnBase):
    pass

class DocTypeColumnCreateUpdateSch(SQLModel):
    doc_type_id: str | None
    column_types: list[str] | None
