from sqlmodel import SQLModel
from models.memo_dt_model import MemoDtBase, MemoDtFullBase
from schemas.attachment_sch import AttachmentCreateSch

class MemoDetailCreateSch(MemoDtBase):
    attachments: list[AttachmentCreateSch] | None

class MemoDetailSch(MemoDtFullBase):
    pass 

class MemoDetailUpdateSch(MemoDtBase):
    pass

class MemoDetailByIdSch(MemoDtFullBase):
    pass

