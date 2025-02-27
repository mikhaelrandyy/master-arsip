from models.doc_type_jenis_kolom_model import DocTypeJenisKolomLinkBase, DocTypeJenisKolomLinkFullBase
from models.base_model import SQLModel
from schemas.jenis_kolom_sch import jenisKolomByIdForMappingSch


class DocTypeJenisKolomLinkCreateSch(DocTypeJenisKolomLinkBase):
    pass

class DocTypeJenisKolomLinkSch(DocTypeJenisKolomLinkFullBase):
    pass

class DocTypeJenisKolomLinkUpdateSch(DocTypeJenisKolomLinkBase):
    pass

class DocTypeJenisKolomLinkByIdSch(DocTypeJenisKolomLinkFullBase):
    pass

class DocTypeJenisKolomLinkForMappingSch(SQLModel):
    doc_type_id: str | None
    jenis_koloms: list[str] | None
