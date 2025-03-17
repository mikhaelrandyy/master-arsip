from sqlmodel import SQLModel
from models.memo_doc_asal_hak_model import MemoDocAsalHakBase, MemoDocAsalHakFullBase

class MemoDocAsalHakCreateSch(MemoDocAsalHakBase):
    pass

class MemoDocAsalHakSch(MemoDocAsalHakFullBase):
    pass 

class MemoDocAsalHakUpdateSch(MemoDocAsalHakBase):
    id: str | None = None

class MemoDocColumnByIdSch(MemoDocAsalHakFullBase):
    pass
