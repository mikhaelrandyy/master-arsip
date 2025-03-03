from models.doc_archive_model import DocArchiveBase, DocArchiveFullBase
from models.base_model import SQLModel
from schemas.jenis_kolom_sch import JenisKolomCreateSch


class DocumentArsipCreateSch(DocArchiveBase):
    jenis_koloms: list[JenisKolomCreateSch] | None

class DocumentArsipSch(DocArchiveFullBase):
    pass

class DocumentArsipUpdateSch(DocArchiveBase):
    pass

class DocumentArsipByIdSch(DocArchiveFullBase):
    pass

    

