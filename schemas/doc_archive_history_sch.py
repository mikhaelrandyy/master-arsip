from models.doc_archive_history_model import DocArchiveHistoryBase
from datetime import date, datetime

class DocArchiveHistoryCreateSch(DocArchiveHistoryBase):
    pass

class DocArchiveHistorySch(DocArchiveHistoryBase):
    memo_code: str 
    doc_category: str
    outgoing_doc_type: str
    necessity: str 
    return_date: date
    safe_location: str
    last_status_at: datetime | None
    description: str

class DocArchiveHistoryUpdateSch(DocArchiveHistoryBase):
    pass

class DocArchiveHistoryByIdSch(DocArchiveHistoryBase):
    pass