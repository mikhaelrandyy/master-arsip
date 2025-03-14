from sqlmodel import SQLModel
from models.memo_doc_model import MemoDocBase, MemoDocFullBase
from schemas.attachment_sch import MemoAttachmentCreateSch

class MemoDocCreateSch(MemoDocBase):
    memo_attachments: list[MemoAttachmentCreateSch] | None

class MemoDocSch(MemoDocFullBase):
    pass 

class MemoDocUpdateSch(MemoDocBase):
    pass

class MemoDocByIdSch(MemoDocFullBase):
    pass

