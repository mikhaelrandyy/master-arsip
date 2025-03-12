from sqlmodel import SQLModel
from models.memo_detail_model import MemoDetailBase, MemoDetailFullBase
from schemas.attachment_sch import AttachmentCreateSch

class MemoDetailCreateSch(MemoDetailBase):
    attachments: list[AttachmentCreateSch] | None

class MemoDetailSch(MemoDetailFullBase):
    pass 

class MemoDetailUpdateSch(MemoDetailBase):
    pass

class MemoDetailByIdSch(MemoDetailFullBase):
    pass

