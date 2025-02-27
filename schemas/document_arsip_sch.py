from models.document_arsip_model import DocumentArsipBase, DocumentArsipFullBase
from models.base_model import SQLModel
from schemas.jenis_kolom_sch import JenisKolomCreateSch


class DocumentArsipCreateSch(DocumentArsipBase):
    jenis_koloms: list[JenisKolomCreateSch] | None

class DocumentArsipSch(DocumentArsipFullBase):
    pass

class DocumentArsipUpdateSch(DocumentArsipBase):
    pass

class DocumentArsipByIdSch(DocumentArsipFullBase):
    pass

    

