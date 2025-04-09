from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from crud.base_crud import CRUDBase
from models import (
    DocArchive, 
    DocArchiveAttachment, 
    DocArchiveColumn, 
    DocArchiveAsalHak,
    Memo,
    MemoDoc,
    MemoDocColumn,
    MemoDocAsalHak,
    MemoDocAttachment
)
from common.enum import (
    StatusDocArchiveEnum, 
    DocumentCategoryEnum,
    OutgoingToDocTypeEnum, 
    WorkflowLastStatusEnum,
    NecessityEnum
)
from schemas.doc_archive_sch import DocArchiveCreateSch, DocArchiveUpdateSch
import crud


class CRUDDocArchive(CRUDBase[DocArchive, DocArchiveCreateSch, DocArchiveUpdateSch]):
    # async def create_doc_archive(self, *, memo_id:str) -> DocArchive:

    #     memo = await crud.memo.get_by_id(id=memo_id)

    #     for doc_archive in memo.memo_docs:
    #         new_doc_archive = DocArchive.model_validate(doc_archive.model_dump())
    #         new_doc_archive.doc_format_id = memo.doc_format_id
    #         new_doc_archive.company_id = memo.company_id
    #         new_doc_archive.project_id = memo.project_id
    #         new_doc_archive.remarks = memo.remarks
    #         new_doc_archive.jenis_arsip = memo.jenis_arsip
    #         new_doc_archive.status = StatusDocArchiveEnum.AVAILABLE if memo.doc_category == DocumentCategoryEnum.MASUK else StatusDocArchiveEnum.UNAVAILABLE

    #         db.session.flush()
    #         db.session.add(new_doc_archive)

    #         for attachment in doc_archive.memo_doc_attachments:
    #             new_doc_archive_attachment = DocArchiveAttachment(**attachment.model_dump(), doc_archive_id=doc_archive.id)
    #             db.session.add(new_doc_archive_attachment)

    #         for column in doc_archive.memo_doc_columns:
    #             new_doc_archive_column = DocArchiveColumn(**column.model_dump(), doc_archive_id=doc_archive.id)
    #             db.session.add(new_doc_archive_column)

    #         for asal_hak in doc_archive.memo_doc_asal_haks:
    #             new_doc_archive_asal_hak = DocArchiveAsalHak(**asal_hak.model_dump(), doc_archive_id=doc_archive.id)
    #             db.session.add(new_doc_archive_asal_hak)

    #     await db.session.commit()

    #     return doc_archive

    async def notif_from_memo(self, *, memo_id: str):
        current_memo = await crud.memo.get(id=memo_id)
        if not current_memo:
            print(f"{str(memo_id)} Memo not found")
            raise HTTPException(status_code=404, detail="Memo not found")
        
        current_workflow = await crud.workflow.get(id=current_memo.workflow_id)
        if not current_workflow:
            print(f"{str(current_memo.code)} Workflow not found")
            raise HTTPException(status_code=404, detail="Workflow not found")
        if current_workflow.last_status != WorkflowLastStatusEnum.COMPLETED:
            print(f"{str(current_memo.code)} Workflow not already COMPLETED")
            raise HTTPException(status_code=400, detail="Workflow not already COMPLETED")
        
        if current_memo.outgoing_doc_type == OutgoingToDocTypeEnum.ASLI:
            if current_memo.doc_category in [DocumentCategoryEnum.MASUK, DocumentCategoryEnum.MASUK_HOLD]:
                await self.document_in(current_memo=current_memo)
            elif current_memo.doc_category == DocumentCategoryEnum.HOLD:
                await self.document_hold(current_memo=current_memo)
            elif current_memo.doc_category == DocumentCategoryEnum.UNHOLD:
                await self.document_unhold(current_memo=current_memo)
            elif current_memo.doc_category == DocumentCategoryEnum.KEMBALI:
                await self.document_back(current_memo=current_memo)
        
        
    async def document_in(self, *, current_memo: Memo):
        current_memo_docs = await crud.memo_doc.get_by_memo(memo_id=current_memo.id)
        await self.create_doc_archive(current_memo=current_memo, current_memo_docs=current_memo_docs)

        try:
            await db.session.commit()
        except Exception as e:
            print(f"{current_memo.id} {e.args}")
            raise HTTPException(status_code=400, detail=e.args)
    
    async def document_hold(self, *, current_memo: Memo):
        current_memo_docs = await crud.memo_doc.get_by_memo(memo_id=current_memo.id)
        for current_memo_doc in current_memo_docs:
            current_doc_archive = await crud.doc_archive.get(id=current_memo_doc.doc_archive_id)
            if not current_doc_archive:
                print(f"{current_memo_doc.doc_archive_id} from {current_memo.id} not found")
                raise HTTPException(status_code=404, detail="Document Archive not found")
            
            await self.update_doc_archive_available_hold(current_doc_archive=current_doc_archive, updated_by=current_memo.created_by)

        try:
            await db.session.commit()
        except Exception as e:
            print(f"{current_memo.id} {e.args}")
            raise HTTPException(status_code=400, detail=e.args) 
    
    async def document_unhold(self, *, current_memo: Memo):
        current_memo_docs = await crud.memo_doc.get_by_memo(memo_id=current_memo.id)
        for current_memo_doc in current_memo_docs:
            current_doc_archive = await crud.doc_archive.get(id=current_memo_doc.doc_archive_id)
            if not current_doc_archive:
                print(f"{current_memo_doc.doc_archive_id} from {current_memo.id} not found")
                raise HTTPException(status_code=404, detail="Document Archive not found")
            
            await self.update_doc_archive_available(current_doc_archive=current_doc_archive, updated_by=current_memo.created_by)

        try:
            await db.session.commit()
        except Exception as e:
            print(f"{current_memo.id} {e.args}")
            raise HTTPException(status_code=400, detail=e.args) 

    async def document_back(self, *, current_memo: Memo):
        current_memo_docs = await crud.memo_doc.get_by_memo(memo_id=current_memo.id)
        for current_memo_doc in current_memo_docs:
            current_doc_archive = await crud.doc_archive.get(id=current_memo_doc.doc_archive_id)
            if not current_doc_archive:
                print(f"{current_memo_doc.doc_archive_id} from {current_memo.id} not found")
                raise HTTPException(status_code=404, detail="Document Archive not found")
            
            await self.update_doc_archive_available(current_doc_archive=current_doc_archive, updated_by=current_memo.created_by)

        try:
            await db.session.commit()
        except Exception as e:
            print(f"{current_memo.id} {e.args}")
            raise HTTPException(status_code=400, detail=e.args) 


    async def create_doc_archive(self, *, current_memo: Memo, current_memo_docs: list[MemoDoc]):
        # CREATE DOC ARCHIVE
        for current_memo_doc in current_memo_docs:
            new_doc_archive_dict = current_memo_doc.model_dump()
            new_doc_archive = DocArchive.model_validate(new_doc_archive_dict)
            new_doc_archive.doc_format_id = current_memo.doc_format_id
            new_doc_archive.company_id = current_memo.company_id
            new_doc_archive.project_id = current_memo.project_id
            new_doc_archive.remarks = current_memo.remarks
            new_doc_archive.jenis_arsip = current_memo.jenis_arsip
            new_doc_archive.status = StatusDocArchiveEnum.AVAILABLE if current_memo.doc_category == DocumentCategoryEnum.MASUK else StatusDocArchiveEnum.AVAILABLE_HOLD
            new_doc_archive = await crud.doc_archive.create(obj_in=new_doc_archive, created_by=current_memo.created_by, with_commit=False)

            # CREATE DOC ARCHIVE COLUMN
            current_memo_doc_columns = await crud.memo_doc_column.get_by_memo_doc(memo_doc_id=current_memo_doc.id)
            if current_memo_doc_columns:
                await self.create_doc_archive_column(
                    doc_archive=new_doc_archive, 
                    current_memo_doc_columns=current_memo_doc_columns, 
                    created_by=current_memo.created_by
                )

            # CREATE DOC ARCHIVE ATTACHMENT
            current_memo_doc_attachments = await crud.memo_doc_attachment.get_by_memo_doc(memo_doc_id=current_memo_doc.id)
            if current_memo_doc_attachments:
                await self.create_doc_archive_attachment(
                    doc_archive=new_doc_archive,
                    current_memo_doc_attachments=current_memo_doc_attachments,
                    created_by=current_memo.created_by
                )
            
            # CREATE DOC ARCHIVE ASAL HAK
            current_memo_doc_asal_haks = await crud.memo_doc_asal_hak.get_by_memo_doc(memo_doc_id=current_memo_doc.id)
            if current_memo_doc_asal_haks:
                await self.create_doc_archive_asal_hak(
                    doc_archive=new_doc_archive,
                    current_memo_doc_asal_haks=current_memo_doc_asal_haks,
                    create_by=current_memo.created_by
                )

    async def create_doc_archive_column(self, *, doc_archive: DocArchive, current_memo_doc_columns: list[MemoDocColumn], created_by: str):
        for current_memo_doc_column in current_memo_doc_columns:
            new_doc_archive_column_dict = current_memo_doc_column.model_dump()
            new_doc_archive_column = DocArchiveColumn.model_validate(new_doc_archive_column_dict)
            new_doc_archive_column.doc_archive_id = doc_archive.id
            await crud.doc_archive_column.create(obj_in=new_doc_archive_column, created_by=created_by, with_commit=False)

    async def create_doc_archive_attachment(self, *, doc_archive: DocArchive, current_memo_doc_attachments: list[MemoDocAttachment], created_by: str):
        for current_memo_doc_attachment in current_memo_doc_attachments:
            new_doc_archive_attachment_dict = current_memo_doc_attachment.model_dump()
            new_doc_archive_attachment = DocArchiveAttachment.model_validate(new_doc_archive_attachment_dict)
            new_doc_archive_attachment.doc_archive_id = doc_archive.id
            await crud.doc_archive_attachment.create(obj_in=new_doc_archive_attachment, created_by=created_by, with_commit=False)

    async def create_doc_archive_asal_hak(self, *, doc_archive: DocArchive, current_memo_doc_asal_haks: list[MemoDocAsalHak], create_by: str):
        for current_memo_doc_asal_hak in current_memo_doc_asal_haks:
            new_doc_archive_asal_hak_dict = current_memo_doc_asal_hak.model_dump()
            new_doc_archive_asal_hak = DocArchiveAsalHak.model_validate(new_doc_archive_asal_hak_dict)
            new_doc_archive_asal_hak.doc_archive_id = doc_archive.id
            await crud.doc_archive_asal_hak.create(obj_in=new_doc_archive_asal_hak, created_by=create_by, with_commit=False)

    async def update_doc_archive_available(self, *, current_doc_archive: DocArchive, updated_by: str):
        new_doc_archive_dict = current_doc_archive.model_dump()
        new_doc_archive = DocArchive.model_validate(new_doc_archive_dict)
        new_doc_archive.status = StatusDocArchiveEnum.AVAILABLE
        await crud.doc_archive.update(obj_current=current_doc_archive, obj_new=new_doc_archive, updated_by=updated_by, with_commit=False)
  
    async def update_doc_archive_available_hold(self, *, current_doc_archive: DocArchive, updated_by: str):
        new_doc_archive_dict = current_doc_archive.model_dump()
        new_doc_archive = DocArchive.model_validate(new_doc_archive_dict)
        new_doc_archive.status = StatusDocArchiveEnum.AVAILABLE_HOLD
        await crud.doc_archive.update(obj_current=current_doc_archive, obj_new=new_doc_archive, updated_by=updated_by, with_commit=False)
  
    async def update_doc_archive_unavailable(self, *, current_doc_archive: DocArchive, is_transfer: bool | None = False, updated_by: str):
        new_doc_archive_dict = current_doc_archive.model_dump()
        new_doc_archive = DocArchive.model_validate(new_doc_archive_dict)
        new_doc_archive.status = StatusDocArchiveEnum.UNAVAILABLE
        new_doc_archive.is_transfer = is_transfer
        await crud.doc_archive.update(obj_current=current_doc_archive, obj_new=new_doc_archive, updated_by=updated_by, with_commit=False)
    
    async def update_doc_archive_column(self, *, current_doc_archive_column: DocArchiveColumn, updated_by: str):
        pass
    
doc_archive = CRUDDocArchive(DocArchive)
