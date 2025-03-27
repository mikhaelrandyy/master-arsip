from fastapi_async_sqlalchemy import db
from crud.base_crud import CRUDBase
from models import DocArchive, DocArchiveAttachment, DocArchiveColumn, DocArchiveAsalHak
from common.enum import StatusDocArchiveEnum, DocumentCategoryEnum
from schemas.doc_archive_sch import DocArchiveCreateSch, DocArchiveUpdateSch
import crud


class CRUDDocArchive(CRUDBase[DocArchive, DocArchiveCreateSch, DocArchiveUpdateSch]):
    async def create_doc_archive(self, *, memo_id:str) -> DocArchive:

        memo = await crud.memo.get_by_id(id=memo_id)

        for doc_archive in memo.memo_docs:
            new_doc_archive = DocArchive.model_validate(doc_archive.model_dump())
            new_doc_archive.doc_format_id = memo.doc_format_id
            new_doc_archive.company_id = memo.company_id
            new_doc_archive.project_id = memo.project_id
            new_doc_archive.remarks = memo.remarks
            new_doc_archive.jenis_arsip = memo.jenis_arsip
            new_doc_archive.status = StatusDocArchiveEnum.AVAILABLE if memo.doc_category == DocumentCategoryEnum.MASUK else StatusDocArchiveEnum.UNAVAILABLE

            db.session.flush()
            db.session.add(new_doc_archive)

            for attachment in doc_archive.memo_doc_attachments:
                new_doc_archive_attachment = DocArchiveAttachment(**attachment.model_dump(), doc_archive_id=doc_archive.id)
                db.session.add(new_doc_archive_attachment)

            for column in doc_archive.memo_doc_columns:
                new_doc_archive_column = DocArchiveColumn(**column.model_dump(), doc_archive_id=doc_archive.id)
                db.session.add(new_doc_archive_column)

            for asal_hak in doc_archive.memo_doc_asal_haks:
                new_doc_archive_asal_hak = DocArchiveAsalHak(**asal_hak.model_dump(), doc_archive_id=doc_archive.id)
                db.session.add(new_doc_archive_asal_hak)

        await db.session.commit()

        return doc_archive

     
doc_archive = CRUDDocArchive(DocArchive)
