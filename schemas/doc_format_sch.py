from models.doc_format_model import DocFormatBase, DocFormatFullBase
from models.base_model import SQLModel
from common.enum import JenisArsipEnum

class DocFormatCreateSch(DocFormatBase):
    pass

class DocFormatSch(DocFormatFullBase):
    pass

class DocFormatUpdateSch(DocFormatBase):
    pass

class DocFormatByIdSch(DocFormatFullBase):
    pass

class DocFormatForDocTypeSch(SQLModel):
    id: str | None
    jenis_arsip:str | None