from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import (
    MemoDocAttachment
)
from schemas.memo_doc_attachment_sch import MemoDocAttachmentCreateSch, MemoDocAttachmentUpdateSch

class CRUDMemoDocAttachment(CRUDBase[MemoDocAttachment, MemoDocAttachmentCreateSch, MemoDocAttachmentUpdateSch]):
    pass

memo_doc_attachment = CRUDMemoDocAttachment(MemoDocAttachment)