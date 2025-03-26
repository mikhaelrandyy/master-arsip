from models.doc_archive_model import DocArchiveBase, DocArchiveFullBase
from schemas.column_type_sch import ColumnTypeCreateSch
from schemas.doc_archive_column_sch import DocArchiveColumnCreateSch

class DocArchiveCreateSch(DocArchiveBase):
    id:str | None
    doc_archive_columns: list[DocArchiveColumnCreateSch] | None = []

class DocArchiveSch(DocArchiveFullBase):
    pass

class DocArchiveUpdateSch(DocArchiveBase):
    pass

class DocArchiveByIdSch(DocArchiveFullBase):
    doc_archive_columns: list[DocArchiveColumnCreateSch] | None = []

    

