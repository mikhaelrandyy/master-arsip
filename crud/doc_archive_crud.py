from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocArchive, DocArchiveAttachment, DocArchiveColumn, DocArchiveAsalHak
from common.enum import StatusDocArchiveEnum
from schemas.doc_archive_sch import DocArchiveCreateSch, DocArchiveUpdateSch
from schemas.doc_archive_column_sch import DocArchiveColumnCreateSch
from schemas.doc_archive_attachment_sch import DocArchiveAttachmentCreateSch
from schemas.doc_archive_asal_hak_sch import DocArchiveAsalHakCreateSch
import crud


class CRUDDocArchive(CRUDBase[DocArchive, DocArchiveCreateSch, DocArchiveUpdateSch]):
    # async def get_by_id(self, *, id:str) -> DocArchive:

    #     query = select(DocArchive)
    #     query = query.where(DocArchive.id == id)
    #     response = await db.session.execute(query)
    #     return response.scalar_one_or_none()
    
    async def create_doc_archive(self, *, memo_id:str) -> DocArchive:

        memo = await crud.memo.get_by_id(id=memo_id)

        for doc in memo.memo_docs:
            doc_archive = DocArchiveCreateSch(
                                            doc_type_id=doc.doc_type_id, 
                                            doc_format_id=memo.doc_format_id,
                                            doc_no=doc.doc_no,
                                            doc_name=doc.doc_name,
                                            doc_archive_ref_id=None,
                                            unit_id=doc.unit_id,
                                            company_id=memo.company_id,
                                            alashak_id=doc.alashak_id,
                                            vendor_id=doc.vendor_id,
                                            project_id=memo.project_id,
                                            physical_doc_type=doc.physical_doc_type,
                                            remarks=memo.remarks,
                                            jenis_arsip=memo.jenis_arsip,
                                            status=StatusDocArchiveEnum.AVAILABLE,
                                        )
            db.session.flush()
            db.session.add(doc_archive)

            for attachment in doc.memo_doc_attachments:
                new_doc_archive_attachment = DocArchiveAttachment(**attachment.model_dump(), doc_archive_id=doc_archive.id)
                db.session.add(new_doc_archive_attachment)

            for column in doc.memo_doc_columns:
                new_doc_archive_column = DocArchiveColumn(**column.model_dump(), doc_archive_id=doc_archive.id)
                db.session.add(new_doc_archive_column)

            for asal_hak in doc.memo_doc_asal_haks:
                new_doc_archive_asal_hak = DocArchiveAsalHak(**asal_hak.model_dump(), doc_archive_id=doc_archive.id)
                db.session.add(new_doc_archive_asal_hak)

        await db.session.commit()

        return doc_archive

     
doc_archive = CRUDDocArchive(DocArchive)
