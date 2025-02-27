from models.document_type_model import DocumentTypeBase, DocumentTypeFullBase
from models.base_model import SQLModel
from schemas.document_format_sch import DocumentFormatForCreateUpdateDocTypeSch, DocFormatForDocTypeSch

class DocumentTypeCreateSch(DocumentTypeBase):
    doc_formats: list[DocumentFormatForCreateUpdateDocTypeSch] | None

class DocumentTypeSch(DocumentTypeFullBase):
    pass 

class DocumentTypeUpdateSch(DocumentTypeBase):
    doc_formats: list[DocFormatForDocTypeSch] | None

class DocumentTypeByIdSch(DocumentTypeFullBase):
    doc_formats: list[DocumentFormatForCreateUpdateDocTypeSch] | None


