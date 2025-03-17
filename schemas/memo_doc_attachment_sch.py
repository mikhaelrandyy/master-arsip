from models.memo_doc_attachment_model import MemoDocAttachmentBase, MemoDocAttachmentFullBase

class MemoDocAttachmentCreateSch(MemoDocAttachmentBase):
    pass

class MemoDocAttachmentSch(MemoDocAttachmentFullBase):
    pass 

class MemoDocAttachmentUpdateSch(MemoDocAttachmentBase):
    id: str | None = None

class MemoDocAttachmentByIdSch(MemoDocAttachmentFullBase):
    pass

