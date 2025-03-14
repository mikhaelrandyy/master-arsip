from sqlmodel import SQLModel
from models.memo_doc_model import MemoDocBase, MemoDocFullBase
from schemas.attachment_sch import AttachmentCreateSch

class MemoDetailCreateSch(MemoDocBase):
    attachments: list[AttachmentCreateSch] | None

class MemoDetailSch(MemoDocFullBase):
    pass 

class MemoDetailUpdateSch(MemoDocBase):
    pass

class MemoDetailByIdSch(MemoDocFullBase):
    pass

