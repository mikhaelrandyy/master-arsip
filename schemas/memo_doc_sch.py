from sqlmodel import SQLModel
from models.memo_doc_model import MemoDocBase, MemoDocFullBase
from schemas.memo_doc_attachment_sch import MemoDocAttachmentCreateSch, MemoDocAttachmentUpdateSch, MemoDocAttachmentSch
from schemas.memo_doc_column_sch import MemoDocColumnCreateSch, MemoDocColumnUpdateSch, MemoDocColumnSch
from schemas.memo_doc_asal_hak_sch import MemoDocAsalHakCreateSch, MemoDocAsalHakUpdateSch, MemoDocAsalHakSch

class MemoDocCreateSch(MemoDocBase):
    memo_doc_attachments: list[MemoDocAttachmentCreateSch] | None = []
    memo_doc_columns: list[MemoDocColumnCreateSch] | None = []
    memo_doc_asal_haks: list[MemoDocAsalHakCreateSch] | None = []

class MemoDocSch(MemoDocFullBase):
    memo_doc_attachments: list[MemoDocAttachmentSch] | None = []
    memo_doc_columns: list[MemoDocColumnSch] | None = []
    memo_doc_asal_haks: list[MemoDocAsalHakSch] | None = [] 

class MemoDocUpdateSch(MemoDocBase):
    id: str | None = None

    memo_doc_attachments: list[MemoDocAttachmentUpdateSch] | None = []
    memo_doc_columns: list[MemoDocColumnUpdateSch] | None = []
    memo_doc_asal_haks: list[MemoDocAsalHakUpdateSch] | None = []
