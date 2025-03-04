from models.doc_type_model import DocTypeBase, DocTypeFullBase
from models.base_model import SQLModel
from schemas.doc_format_sch import DocFormatSch, DocFormatForDocTypeSch
from schemas.column_type_sch import ColumnTypeSch

class DocTypeCreateSch(DocTypeBase):
    document_formats: list[DocFormatForDocTypeSch] | None

class DocTypeSch(DocTypeFullBase):
    jumlah_jenis_koloms: int | None
    jenis_koloms: list[ColumnTypeSch] | None

class DocTypeUpdateSch(DocTypeBase):
    document_formats: list[DocFormatForDocTypeSch] | None

class DocTypeByIdSch(DocTypeFullBase):
    document_formats: list[DocFormatSch] | None

class DocTypeCreateForDepartementSch(DocTypeBase):
    id:str | None