from sqlmodel import SQLModel
from models.memo_doc_model import MemoDocBase, MemoDocFullBase
from schemas.memo_doc_attachment_sch import MemoDocAttachmentCreateSch

class MemoDocCreateSch(MemoDocBase):
    memo_doc_attachments: list[MemoDocAttachmentCreateSch] | None = []

class MemoDocSch(MemoDocFullBase):
    pass 

class MemoDocUpdateSch(MemoDocBase):
    id: str | None = None

class MemoDocByIdSch(MemoDocFullBase):
    pass
