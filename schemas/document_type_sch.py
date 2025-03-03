from models.doc_type_model import DocTypeBase, DocTypeFullBase
from models.base_model import SQLModel
from schemas.document_format_sch import DocumentFormatSch, DocFormatForDocTypeSch
from schemas.jenis_kolom_sch import JenisKolomSch

class DocumentTypeCreateSch(DocTypeBase):
    document_formats: list[DocFormatForDocTypeSch] | None

class DocumentTypeSch(DocTypeFullBase):
    jumlah_jenis_koloms: int | None
    jenis_koloms: list[JenisKolomSch] | None

class DocumentTypeUpdateSch(DocTypeBase):
    document_formats: list[DocFormatForDocTypeSch] | None

class DocumentTypeByIdSch(DocTypeFullBase):
    document_formats: list[DocumentFormatSch] | None
