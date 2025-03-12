from sqlmodel import SQLModel
from models.memo_attachment_model import MemoAttachmentBase, MemoAttachmentFullBase

class AttachmentCreateSch(MemoAttachmentBase):
    pass

class AttachmentSch(MemoAttachmentFullBase):
    pass 

class AttachmentUpdateSch(MemoAttachmentBase):
    pass

class AttachmentByIdSch(MemoAttachmentFullBase):
    pass

