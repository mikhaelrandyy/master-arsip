from sqlmodel import SQLModel
from models.attachment_model import AttachmentBase, AttachmentFullBase

class AttachmentCreateSch(AttachmentBase):
    pass

class AttachmentSch(AttachmentFullBase):
    pass 

class AttachmentUpdateSch(AttachmentBase):
    pass

class AttachmentByIdSch(AttachmentFullBase):
    pass

