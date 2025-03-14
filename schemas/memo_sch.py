from models.memo_model import MemoBase, MemoFullBase
from schemas.doc_detail_sch import MemoDocCreateSch

class MemoCreateSch(MemoBase):
    memo_docs: list[MemoDocCreateSch] | None

class MemoSch(MemoFullBase):
    project_code: str | None = None
    company_code: str | None = None

class MemoUpdateSch(MemoBase):
    pass

class MemoByIdSch(MemoFullBase):
    project_code: str | None
    company_code: str | None

