from models.document_format_model import DocumentFormatBase, DocumentFormatFullBase
from models.base_model import SQLModel
from common.enum import JenisArsipEnum



class DocumentFormatCreateSch(DocumentFormatBase):
    pass

class DocumentFormatSch(DocumentFormatFullBase):
    jenis_arsip:str | None

class DocumentFormatUpdateSch(DocumentFormatBase):
    pass

class DocumentFormatByIdSch(DocumentFormatFullBase):
    pass

class DocFormatForDocTypeSch(SQLModel):
    id: str | None
    jenis_arsip:str | None