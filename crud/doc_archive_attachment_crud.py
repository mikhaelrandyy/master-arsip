from crud.base_crud import CRUDBase
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models import DocArchiveAttachment
from schemas.doc_archive_attachment_sch import DocArchiveAttachmentCreateSch, DocArchiveAttachmentUpdateSch

class CRUDDocArchiveAttachment(CRUDBase[DocArchiveAttachment, DocArchiveAttachmentCreateSch, DocArchiveAttachmentUpdateSch]):    
    pass

doc_archive_attachment = CRUDDocArchiveAttachment(DocArchiveAttachment)