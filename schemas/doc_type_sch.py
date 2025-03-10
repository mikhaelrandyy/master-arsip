from models.doc_type_model import DocTypeBase, DocTypeFullBase
from models.base_model import SQLModel
from schemas.doc_type_archive_sch import DocTypeArchiveSch, DocTypeArchiveCreateSch, DocTypeArchiveUpdateSch
from schemas.doc_type_column_sch import DocTypeColumnSch

class DocTypeCreateSch(DocTypeBase):
    doc_archives: list[DocTypeArchiveCreateSch] | None = []

class DocTypeSch(DocTypeFullBase):
    doc_type_group_name: str | None = None
    number_of_columns: int | None = None

class DocTypeByIdSch(DocTypeSch):
    doc_archives: list[DocTypeArchiveSch] | None = None
    doc_columns: list[DocTypeColumnSch] | None = None

class DocTypeUpdateSch(DocTypeBase):
    doc_archives: list[DocTypeArchiveUpdateSch] | None = []