from models.memo_model import MemoBase, MemoFullBase
from schemas.doc_detail_sch import MemoDocCreateSch, MemoDocSch

class MemoCreateSch(MemoBase):
    memo_docs: list[MemoDocCreateSch] | None

class MemoSch(MemoFullBase):
    project_code: str | None = None
    company_code: str | None = None

class MemoUpdateSch(MemoBase):
    memo_docs: list[MemoDocSch] | None = None

class MemoByIdSch(MemoFullBase):
    project_code: str | None
    company_code: str | None
    memo_docs: list[MemoDocCreateSch] | None = None



