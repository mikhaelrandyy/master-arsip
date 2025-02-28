from models.doc_type_jenis_kolom_model import DoctypeJeniskolomBase
from models.base_model import SQLModel


class DocTypeJenisKolomCreateSch(DoctypeJeniskolomBase):
    pass

class DocTypeJenisKolomSch(DoctypeJeniskolomBase):
    pass

class DocTypeJenisKolomUpdateSch(DoctypeJeniskolomBase):
    pass

class DocTypeJenisKolomByIdSch(DoctypeJeniskolomBase):
    pass

class DocTypeJenisKolomForMappingSch(SQLModel):
    doc_type_id: str | None
    jenis_koloms: list[str] | None

class DocTypeJenisKolomMappingSch(SQLModel):
    document_type_name: str | None
    doc_type_id: str | None
    jumlah_jenis_kolom: int | None
