from models.document_format_model import DocumentFormatBase, DocumentFormatFullBase
from models.base_model import SQLModel
from common.enum import JenisArsipEnum



class DocumentFormatCreateSch(DocumentFormatBase):
    pass

class DocumentFormatSch(DocumentFormatFullBase):
    pass

class DocumentFormatUpdateSch(DocumentFormatBase):
    pass

class DocumentFormatByIdSch(DocumentFormatFullBase):
    pass

class DocumentFormatForDocTypeSch(DocumentFormatBase):
    id: str | None
    jenis_arsip:JenisArsipEnum
