from crud.base_crud import CRUDBase
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models import DocArchiveAsalHak
from schemas.doc_archive_asal_hak_sch import DocArchiveAsalHakCreateSch, DocArchiveAsalHakUpdateSch

class CRUDDocArchiveAsalHak(CRUDBase[DocArchiveAsalHak, DocArchiveAsalHakCreateSch, DocArchiveAsalHakUpdateSch]):    
    pass

doc_archive_asal_hak = CRUDDocArchiveAsalHak(DocArchiveAsalHak)