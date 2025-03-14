from models.memo_doc_model import MemoDocBase, MemoDocFullBase
from schemas.doc_detail_sch import MemoDocCreateSch, MemoDocSch

class MemoDocCreateSch(MemoDocBase):
    pass

class MemoDocSch(MemoDocBase):
    pass

class MemoDocUpdateSch(MemoDocBase):
    pass

class MemoDocByIdSch(MemoDocFullBase):
    pass



