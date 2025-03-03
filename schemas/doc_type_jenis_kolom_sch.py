from models.doc_type_column_model import DocTypeColumnBase
from models.base_model import SQLModel


class DocTypeJenisKolomCreateSch(DocTypeColumnBase):
    pass

class DocTypeJenisKolomSch(DocTypeColumnBase):
    pass

class DocTypeJenisKolomUpdateSch(DocTypeColumnBase):
    jenis_koloms: list[str] | None


class DocTypeJenisKolomByIdSch(DocTypeColumnBase):
    pass

class DocTypeJenisKolomForMappingSch(SQLModel):
    doc_type_id: str | None
    jenis_koloms: list[str] | None