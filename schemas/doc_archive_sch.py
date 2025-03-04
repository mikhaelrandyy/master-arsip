from models.doc_archive_model import DocArchiveBase, DocArchiveFullBase
from models.base_model import SQLModel
from schemas.column_type_sch import ColumnTypeCreateSch


class DocArchiveCreateSch(DocArchiveBase):
    jenis_koloms: list[ColumnTypeCreateSch] | None

class DocArchiveSch(DocArchiveFullBase):
    pass

class DocArchiveUpdateSch(DocArchiveBase):
    pass

class DocArchiveByIdSch(DocArchiveFullBase):
    pass

    

