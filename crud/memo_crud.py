from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import selectinload, joinedload
from fastapi_pagination import Params, Page
from crud.base_crud import CRUDBase
from sqlmodel import and_, select, cast, String, or_, func
from models import Memo, MemoDoc, MemoDocAttachment, Project, Company
from common.generator import generate_code
from common.enum import CodeCounterEnum
from schemas.memo_sch import MemoCreateSch, MemoUpdateSch, MemoByIdSch
from schemas.memo_doc_sch import MemoDocCreateSch, MemoDocUpdateSch, MemoDocSch
from schemas.memo_doc_attachment_sch import MemoDocAttachmentCreateSch, MemoDocAttachmentUpdateSch, MemoDocAttachmentSch
from schemas.oauth import AccessToken
import crud

class CRUDMemo(CRUDBase[Memo, MemoCreateSch, MemoUpdateSch]):
    async def create(self, *, memo:MemoCreateSch, created_by:str) -> Memo:

        memo.code = await generate_code(entity=CodeCounterEnum.MEMO)

        db_obj = Memo.model_validate(memo)

        if created_by:
            db_obj.created_by = db_obj.updated_by = created_by

        db.session.add(db_obj)
        await db.session.flush()

        if memo.memo_docs:
            await self.create_memo_docs(memo_docs=memo.memo_docs, memo_id=db_obj.id, created_by=created_by)

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

        for doc in obj_new.memo_docs:
            memo_doc = await crud.memo_doc.get(id=doc.id) if doc.id else None

            if not memo_doc:
                db_obj_doc = MemoDoc(**doc.model_dump())
                db_obj_doc.memo_id = obj_current.id
                
                if updated_by:
                    db_obj_doc.created_by = db_obj_doc.updated_by = updated_by
            else:
                pass
                
        for remove in current_memo_docs:
            await db.session.delete(remove)

        # await db.session.commit()
        await db.session.refresh(obj_current)

        return obj_current
    
    async def create_memo_docs(self, *, 
                            memo_docs: list[MemoDocCreateSch], 
                            memo_id: str, 
                            created_by: str):
        
        for doc in memo_docs:
            db_obj_doc = MemoDoc(**doc.model_dump())
            db_obj_doc.memo_id = memo_id

            if created_by:
                db_obj_doc.created_by = db_obj_doc.updated_by = created_by

            db.session.add(db_obj_doc)
            await db.session.flush()

            if doc.memo_doc_attachments:
                await self.create_memo_doc_attachments(memo_doc_attachments=doc.memo_doc_attachments, memo_doc_id=db_obj_doc.id, created_by=created_by)

    async def create_memo_doc_attachments(self, *, 
                                        memo_doc_attachments: list[MemoDocAttachmentCreateSch], 
                                        memo_doc_id: str, 
                                        created_by: str):
        
        for doc_attachment in memo_doc_attachments:
                db_obj_doc_attachment = MemoDocAttachment(**doc_attachment.model_dump())
                db_obj_doc_attachment.memo_doc_id = memo_doc_id

                if created_by:
                    db_obj_doc_attachment.created_by = db_obj_doc_attachment.updated_by = created_by

                db.session.add(db_obj_doc_attachment)
                await db.session.flush()
    
    async def update_memo_docs(self, *,
                               memo_docs: list[MemoDocUpdateSch],
                               memo_id: str,
                               updated_by: str):
        
        current_memo_docs = await crud.memo_doc.get_by_memo(memo_id=memo_id)

        for doc in memo_docs:
            memo_doc = await crud.memo_doc.get(id=doc.id) if doc.id else None

            if not memo_doc:
                db_obj_doc = MemoDoc(**doc.model_dump())
                db_obj_doc.memo_id = memo_id
                
                if updated_by:
                    db_obj_doc.created_by = db_obj_doc.updated_by = updated_by
            else:
                pass
                
        for remove in current_memo_docs:
            await db.session.delete(remove)
        

    async def get_by_id(self, *, id:str):
        memo = await self.fetch_memo(id=id)
        if not memo: 
            return None
        
        memo = MemoByIdSch(**memo._mapping)
        memo.memo_docs = await self.fetch_memo_docs(memo_id=id)
        
        return memo
    
    async def fetch_memo(self, **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs)

        response = await db.session.execute(query)

        return response.one_or_none()
    
    # async def fetch_memo_docs(self, memo_id:str):

    #     memo_documents = []

    #     memo_docs = await crud.memo_doc.fetch_memo_id(memo_id=memo_id)
    #     if not memo_docs: 
    #         return []
        
    #     for memo_doc in memo_docs:
    #         doc = MemoDocSch(
    #                 memo_id=memo_doc.get("memo_id", ""),
    #                 doc_archive_id=memo_doc.get("doc_archive_id", None),
    #                 doc_type_id=memo_doc.get("doc_type_id", ""),
    #                 doc_no=memo_doc.get("doc_no", ""),
    #                 doc_name=memo_doc.get("doc_name", None),
    #                 unit_id=memo_doc.get("unit_id", None),
    #                 alashak_id=memo_doc.get("alashak_id", None),
    #                 physical_doc_type=memo_doc.get("physical_doc_type"),
    #                 remarks=memo_doc.get("remarks", ""),
    #                 vendor_id=memo_doc.get("vendor_id", None)
    #             )
    #         # doc = MemoDocSch(**memo_doc)
    #         memo_documents.append(doc)

    #     return memo_documents

    async def get_paginated(self, *, params: Params | None = Params(), **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs)

        return await paginate(db.session, query, params)
    
    def base_query(self):

        query = select(
                    *Memo.__table__.columns,
                    Project.code.label('project_code'),
                    Company.code.label('company_code')
                )
        
        query = query.outerjoin(Project, Project.id == Memo.project_id,
                            ).outerjoin(Company, Company.id == Memo.company_id)
        return query

    def create_filter(self, *, query, filter:dict):
        
        if filter.get("id"):
            memo_id = filter.get("id")
            query = query.filter(Memo.id == memo_id)

        if filter.get("search"):
            search = filter.get("search")
            query = query.filter(
                or_(
                    cast(Memo.no_memo, String).ilike(f'%{search}%'),
                    cast(Memo.created_by, String).ilike(f'%{search}%')
                )
            )
            
        if filter.get("order_by"):
            order_column = getattr(Memo, filter.get('order_by'))
            query = query.order_by(order_column.desc())

        return query
    
memo = CRUDMemo(Memo)
