from models.memo_model import MemoBase, MemoFullBase
from schemas.memo_doc_sch import MemoDocCreateSch, MemoDocUpdateSch

class MemoCreateSch(MemoBase):
    memo_docs: list[MemoDocCreateSch] | None = []

class MemoSch(MemoFullBase):
    project_code: str | None = None
    company_code: str | None = None

class MemoUpdateSch(MemoBase):
    memo_docs: list[MemoDocUpdateSch] | None = []

class MemoByIdSch(MemoFullBase):
    project_code: str | None
    company_code: str | None
    memo_docs: list[MemoDocCreateSch] | None = None



