from models.memo_model import MemoBase, MemoFullBase
from schemas.doc_detail_sch import MemoDetailCreateSch

class MemoCreateSch(MemoBase):
    memo_details: list[MemoDetailCreateSch] | None

class MemoSch(MemoFullBase):
    project_code: str | None
    company_code: str | None

class MemoUpdateSch(MemoBase):
    pass

class MemoByIdSch(MemoFullBase):
    project_code: str | None
    company_code: str | None

