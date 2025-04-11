from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import selectinload, joinedload
from fastapi_pagination import Params, Page
from crud.base_crud import CRUDBase
from sqlmodel import and_, select, cast, String, or_, func, case
from models import (
    Memo, 
    MemoDoc, 
    MemoDocColumn,
    MemoDocAsalHak,
    MemoDocAttachment, 
    Project, 
    Company,
    Workflow,
    Worker
)
from common.generator import generate_code
from common.enum import CodeCounterEnum, WorkflowLastStatusEnum, WorkflowEntityEnum
from schemas.common_sch import OrderEnumSch
from schemas.memo_sch import MemoCreateSch, MemoUpdateSch, MemoByIdSch
from schemas.memo_doc_sch import MemoDocCreateSch, MemoDocUpdateSch, MemoDocSch
from schemas.memo_doc_column_sch import MemoDocColumnCreateSch, MemoDocColumnUpdateSch, MemoDocColumnSch
from schemas.memo_doc_attachment_sch import MemoDocAttachmentCreateSch, MemoDocAttachmentUpdateSch, MemoDocAttachmentSch
from schemas.memo_doc_asal_hak_sch import MemoDocAsalHakCreateSch, MemoDocAsalHakUpdateSch, MemoDocAsalHakSch
from schemas.workflow_sch import WorkflowCreateSch
from schemas.oauth import AccessToken
from datetime import datetime, timezone
import crud

class CRUDMemo(CRUDBase[Memo, MemoCreateSch, MemoUpdateSch]):
    async def create(self, *, memo:MemoCreateSch, created_by:str) -> Memo:

        memo.code = await generate_code(entity=CodeCounterEnum.MEMO)
        db_obj = Memo.model_validate(memo)

        if created_by:
            db_obj.created_by = db_obj.updated_by = created_by

        db.session.add(db_obj)
        await db.session.flush()

        for memo_doc in memo.memo_docs:
            new_memo_doc = MemoDoc(**memo_doc.model_dump(), memo_id=db_obj.id)
            new_memo_doc = await crud.memo_doc.create(
                obj_in=new_memo_doc, 
                created_by=created_by, 
                with_commit=False
            )

            for memo_doc_column in memo_doc.memo_doc_columns:
                new_memo_doc_column = MemoDocColumn(**memo_doc_column.model_dump(), memo_doc_id=new_memo_doc.id)
                memo_doc_column.memo_doc_id = new_memo_doc.id
                await crud.memo_doc_column.create(
                    obj_in=new_memo_doc_column,
                    created_by=created_by,
                    with_commit=False
                )
            
            for memo_doc_attachment in memo_doc.memo_doc_attachments:
                new_memo_doc_attachment = MemoDocAttachment(**memo_doc_attachment.model_dump(), memo_doc_id=new_memo_doc.id)
                await crud.memo_doc_attachment.create(
                    obj_in=new_memo_doc_attachment,
                    created_by=created_by,
                    with_commit=False
                )
            
            for memo_doc_asal_hak in memo_doc.memo_doc_asal_haks:
                new_memo_doc_asal_hak = MemoDocAsalHak(**memo_doc_asal_hak.model_dump(), memo_doc_id=new_memo_doc.id)
                await crud.memo_doc_asal_hak.create(
                    obj_in=new_memo_doc_asal_hak,
                    created_by=created_by,
                    with_commit=False
                )

        await db.session.commit()
        await db.session.refresh(db_obj)
        return db_obj
    
    async def update(self, *, obj_current: Memo, obj_new: MemoUpdateSch, updated_by: str) -> Memo:

        obj_data = jsonable_encoder(obj_current)
        update_data = obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])
            elif updated_by and updated_by != "" and field == "updated_by":
                setattr(obj_current, field, updated_by)

        db.session.add(obj_current)
        await db.session.flush()

        current_memo_docs = await crud.memo_doc.get_by_memo(memo_id=obj_current.id)
        current_memo_doc_columns = await crud.memo_doc_column.get_by_memo(memo_id=obj_current.id)
        current_memo_doc_attachments = await crud.memo_doc_attachment.get_by_memo(memo_id=obj_current.id)
        current_memo_doc_asal_haks = await crud.memo_doc_asal_hak.get_by_memo(memo_id=obj_current.id)

        for memo_doc in obj_new.memo_docs:
            obj_current_memo_doc = await crud.memo_doc.get(id=memo_doc.id) if memo_doc.id else None
            new_memo_doc = MemoDoc(**memo_doc.model_dump())
            new_memo_doc.memo_id=obj_current.id
            if not obj_current_memo_doc:
                new_memo_doc = await crud.memo_doc.create(
                    obj_in=new_memo_doc, 
                    created_by=updated_by, 
                    with_commit=False
                )
            else:
                new_memo_doc = await crud.memo_doc.update(
                    obj_current=obj_current_memo_doc, 
                    obj_new=new_memo_doc,
                    updated_by=updated_by,
                    with_commit=False
                )
                current_memo_docs.remove(obj_current_memo_doc)

            for memo_doc_column in memo_doc.memo_doc_columns:
                obj_current_memo_doc_column = await crud.memo_doc_column.get(id=memo_doc_column.id)
                new_memo_doc_column = MemoDocColumn(**memo_doc_column.model_dump())
                new_memo_doc_column.memo_doc_id=new_memo_doc.id
                if not obj_current_memo_doc_column:
                    await crud.memo_doc_column.create(
                        obj_in=new_memo_doc_column,
                        created_by=updated_by,
                        with_commit=False
                    )
                else:
                    await crud.memo_doc_column.update(
                        obj_current=obj_current_memo_doc_column,
                        obj_new=new_memo_doc_column,
                        updated_by=updated_by,
                        with_commit=False
                    )
                    current_memo_doc_columns.remove(obj_current_memo_doc_column)
            
            for memo_doc_attachment in memo_doc.memo_doc_attachments:
                obj_current_memo_doc_attachment = await crud.memo_doc_attachment.get(id=memo_doc_attachment.id)
                new_memo_doc_attachment = MemoDocAttachment(**memo_doc_attachment.model_dump())
                new_memo_doc_attachment.memo_doc_id=new_memo_doc.id
                if not obj_current_memo_doc_attachment:
                    await crud.memo_doc_attachment.create(
                        obj_in=new_memo_doc_attachment,
                        created_by=updated_by,
                        with_commit=False
                    )
                else:
                    await crud.memo_doc_attachment.update(
                        obj_current=obj_current_memo_doc_attachment,
                        obj_new=new_memo_doc_attachment,
                        updated_by=updated_by,
                        with_commit=False
                    )
            
            for memo_doc_asal_hak in memo_doc.memo_doc_asal_haks:
                obj_current_memo_doc_asal_hak = await crud.memo_doc_asal_hak.get(id=memo_doc_asal_hak.id)
                new_memo_doc_asal_hak = MemoDocAsalHak(**memo_doc_asal_hak.model_dump())
                new_memo_doc_asal_hak.memo_doc_id=new_memo_doc.id
                if not obj_current_memo_doc_asal_hak:
                    await crud.memo_doc_asal_hak.create(
                        obj_in=new_memo_doc_asal_hak,
                        created_by=updated_by,
                        with_commit=False
                    )
                else:
                    await crud.memo_doc_asal_hak.update(
                        obj_current=obj_current_memo_doc_asal_hak,
                        obj_new=new_memo_doc_asal_hak,
                        updated_by=updated_by,
                        with_commit=False
                    )

        for column in current_memo_doc_columns:
            await db.session.delete(column)

        for attachment in current_memo_doc_attachments:
            await db.session.delete(attachment)

        for asal_hak in current_memo_doc_asal_haks:
            await db.session.delete(asal_hak)        
        
        for doc in current_memo_docs:
            await db.session.delete(doc)

        await db.session.commit()
        await db.session.refresh(obj_current)

        return obj_current
    
    async def submit(self, *, obj_current: Memo, updated_by: str) -> Memo:
        
        workflow = await self.create_workflow(reference_id=obj_current.id, created_by=updated_by)
        obj_updated = Memo.model_validate(obj_current)
        obj_updated.workflow_id = workflow.id

        obj_updated = await self.update(obj_current=obj_current, obj_new=obj_updated, updated_by=updated_by)
        return obj_updated
        
    async def create_workflow(self, *, reference_id: str, created_by: str | None = None):
        template = await crud.workflow_template.get_by_entity(entity=WorkflowEntityEnum.MEMO)
        sch = WorkflowCreateSch(
            reference_id=reference_id, 
            entity=template.entity, 
            flow_id=template.flow_id, 
            version=1, 
            last_status=WorkflowLastStatusEnum.ISSUED, 
            step_name="ISSUED"
        )

        workflow = await crud.workflow.create(obj_in=sch, created_by=created_by, with_commit=False)
        return workflow


    async def get_by_id(self, *, id:str):
        memo = await self.fetch_memo(id=id)
        if not memo: 
            return None
        
        memo = MemoByIdSch(**memo._mapping)
        memo.memo_docs = await self.fetch_memo_docs(memo_id=id)
        
        return memo
     
    async def get_paginated(self, *, params: Params | None = Params(), login_user: AccessToken | None = None, **kwargs):
        query = self.base_query()
        query = self.create_filter(login_user=login_user, query=query, filter=kwargs)

        return await paginate(db.session, query, params)
    
    async def get_no_paginated(self, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs)
        response = await db.session.execute(query)

        return response.mappings().all()
    
    def base_query(self):

        query = select(
                *Memo.__table__.columns,
                Project.code.label('project_code'),
                Company.code.label('company_code'),
                case((Workflow.last_status.in_([WorkflowLastStatusEnum.COMPLETED, WorkflowLastStatusEnum.REJECTED]), Workflow.last_status),
                else_ = Workflow.step_name).label("workflow_status"),
            )
        
        query = query.outerjoin(Project, Project.id == Memo.project_id
                    ).outerjoin(Company, Company.id == Memo.company_id
                    ).outerjoin(Workflow, Workflow.id == Memo.workflow_id
                    ).outerjoin(Worker, Worker.id == Memo.created_by
                    ).distinct()
        
        return query

    def create_filter(self, *, login_user: AccessToken | None = None, query, filter:dict):
        if filter.get("search"):
            search = filter.get("search")
            query = query.filter(
                or_(
                    cast(Memo.code, String).ilike(f'%{search}%'),
                    cast(Memo.created_by, String).ilike(f'%{search}%')
                )
            )
            
        if filter.get("order_by"):
            if filter.get("order"):
                order_column = getattr(Memo, filter.get('order_by'), None)
                if order_column is None:
                    raise HTTPException(status_code=400, detail=f'Field {filter.get("order_by")} not found')
                order = filter.get("order")
                if order == OrderEnumSch.descendent:
                  query = query.order_by(order_column.desc())
                if order == OrderEnumSch.ascendent:
                  query = query.order_by(order_column.asc())

        if login_user and login_user.authorities and 'superadmin' not in login_user.authorities:
            query = query.filter(Memo.created_by == login_user.client_id)

        return query
    
    async def fetch_memo(self, id: str):
        query = self.base_query()
        query = query.where(Memo.id == id)
        response = await db.session.execute(query)

        return response.one_or_none()
    
    async def fetch_memo_docs(self, memo_id: str):
        docs = await crud.memo_doc.fetch_by_memo(memo_id=memo_id)
        if not docs:
            return []
        
        memo_docs = []
        for memo_doc in docs:
            memo_doc = MemoDocSch(**memo_doc)
            memo_doc.memo_doc_columns = await self.fetch_memo_doc_columns(memo_doc_id=memo_doc.id)
            memo_doc.memo_doc_attachments = await self.fetch_memo_doc_attachments(memo_doc_id=memo_doc.id)
            memo_doc.memo_doc_asal_haks = await self.fetch_memo_doc_asal_haks(memo_doc_id=memo_doc.id)
            memo_docs.append(memo_doc)

        return memo_docs

    async def fetch_memo_doc_columns(self, memo_doc_id: str):
        columns = await crud.memo_doc_column.fetch_by_memo_doc(memo_doc_id=memo_doc_id)
        if not columns:
            return []
        
        memo_doc_columns = []
        for memo_doc_column in columns:
            memo_doc_column = MemoDocColumnSch(**memo_doc_column)
            memo_doc_columns.append(memo_doc_column)

        return memo_doc_columns
    
    async def fetch_memo_doc_attachments(self, memo_doc_id: str):
        attachments = await crud.memo_doc_attachment.fetch_by_memo_doc(memo_doc_id=memo_doc_id)
        if not attachments:
            return []
        
        memo_doc_attachments = []
        for memo_doc_attachment in attachments:
            memo_doc_attachment = MemoDocAttachmentSch(**memo_doc_attachment)
            memo_doc_attachments.append(memo_doc_attachment)

        return memo_doc_attachments
   
    async def fetch_memo_doc_asal_haks(self, memo_doc_id: str):
        asal_haks = await crud.memo_doc_asal_hak.fetch_by_memo_doc(memo_doc_id=memo_doc_id)
        if not asal_haks:
            return []
        
        memo_doc_asal_haks = []
        for memo_doc_asal_hak in asal_haks:
            memo_doc_asal_hak = MemoDocAsalHakSch(**memo_doc_asal_hak)
            memo_doc_asal_haks.append(memo_doc_asal_hak)

        return memo_doc_asal_haks

memo = CRUDMemo(Memo)
