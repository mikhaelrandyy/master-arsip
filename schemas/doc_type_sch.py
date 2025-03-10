from models.doc_type_model import DocTypeBase, DocTypeFullBase
from models.base_model import SQLModel
from schemas.doc_type_archive_sch import DocTypeArchiveSch, DocTypeArchiveCreateSch, DocTypeArchiveUpdateSch
from schemas.column_type_sch import ColumnTypeSch

class DocTypeCreateSch(DocTypeBase):
    doc_archives: list[DocTypeArchiveCreateSch] | None

class DocTypeSchFullBaseSch(DocTypeFullBase):
    doc_type_group_name: str | None
    number_of_columns: int | None

class DocTypeSch(DocTypeSchFullBaseSch):
    doc_archives: list[DocTypeArchiveSch] | None
    column_types: list[ColumnTypeSch] | None

class DocTypeUpdateSch(DocTypeBase):
    doc_archives: list[DocTypeArchiveUpdateSch] | None