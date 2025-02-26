from models.document_type_model import DocumentTypeBase, DocumentTypeFullBase
from models.base_model import SQLModel
from schemas.document_format_sch import DocumentFormatForDocTypeSch


class DocumentTypeCreateSch(DocumentTypeBase):
    doc_formats: list[DocumentFormatForDocTypeSch] | None

class DocumentTypeSch(DocumentTypeFullBase):
    pass 

class DocumentTypeUpdateSch(DocumentTypeBase):
    pass

class DocumentTypeByIdSch(DocumentTypeFullBase):
    pass

