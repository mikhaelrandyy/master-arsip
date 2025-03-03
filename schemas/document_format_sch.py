from models.doc_format_model import DocFormatBase, DocFormatFullBase
from models.base_model import SQLModel
from common.enum import JenisArsipEnum



class DocumentFormatCreateSch(DocFormatBase):
    pass

class DocumentFormatSch(DocFormatFullBase):
    jenis_arsip:str | None

class DocumentFormatUpdateSch(DocFormatBase):
    pass

class DocumentFormatByIdSch(DocFormatFullBase):
    pass

class DocFormatForDocTypeSch(SQLModel):
    id: str | None
    jenis_arsip:str | None