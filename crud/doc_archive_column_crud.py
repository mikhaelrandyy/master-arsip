from crud.base_crud import CRUDBase
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models import DocArchiveColumn
from schemas.doc_archive_column_sch import DocArchiveColumnCreateSch, DocArchiveColumnUpdateSch

class CRUDDocArchiveColumn(CRUDBase[DocArchiveColumn, DocArchiveColumnCreateSch, DocArchiveColumnUpdateSch]):    
    pass

doc_archive_column = CRUDDocArchiveColumn(DocArchiveColumn)