from models.memo_model import MemoBase, MemoFullBase
from schemas.memo_doc_sch import MemoDocCreateSch, MemoDocUpdateSch, MemoDocSch

class MemoCreateSch(MemoBase):
    memo_docs: list[MemoDocCreateSch] | None = None

class MemoSch(MemoFullBase):
    project_code: str | None = None
    company_code: str | None = None
    workflow_status: str | None = None

class MemoUpdateSch(MemoBase):
    memo_docs: list[MemoDocUpdateSch] | None = None

class MemoByIdSch(MemoSch):
    memo_docs: list[MemoDocSch] | None = None


