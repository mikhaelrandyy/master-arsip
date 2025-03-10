from models.doc_type_archive_model import DocTypeArchiveBase
from models.base_model import SQLModel


class DocTypeArchiveCreateSch(DocTypeArchiveBase):
    pass

class DocTypeArchiveSch(DocTypeArchiveBase):
    doc_format_name: str | None = None

class DocTypeArchiveUpdateSch(DocTypeArchiveBase):
    id: str | None = None

class DocTypeArchiveByIdSch(DocTypeArchiveBase):
    pass

