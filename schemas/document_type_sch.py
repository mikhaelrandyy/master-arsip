from models.document_type_model import DocumentTypeBase, DocumentTypeFullBase
from models.base_model import SQLModel
from schemas.document_format_sch import DocumentFormatSch, DocFormatForDocTypeSch

class DocumentTypeCreateSch(DocumentTypeBase):
    document_formats: list[DocFormatForDocTypeSch] | None

class DocumentTypeSch(DocumentTypeFullBase):
    pass 

class DocumentTypeUpdateSch(DocumentTypeBase):
    document_formats: list[DocFormatForDocTypeSch] | None

class DocumentTypeByIdSch(DocumentTypeFullBase):
    document_formats: list[DocumentFormatSch] | None
