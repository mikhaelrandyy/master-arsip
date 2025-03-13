from sqlmodel import SQLModel
from models.memo_doc_attachment_model import MemoDocAttachmentBase, MemoDocAttachmentFullBase

class AttachmentCreateSch(MemoDocAttachmentBase):
    pass

class AttachmentSch(MemoDocAttachmentFullBase):
    pass 

class AttachmentUpdateSch(MemoDocAttachmentBase):
    pass

class AttachmentByIdSch(MemoDocAttachmentFullBase):
    pass

