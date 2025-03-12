from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import selectinload, joinedload
from fastapi_pagination import Params, Page
from crud.base_crud import CRUDBase
from sqlmodel import and_, select, cast, String, or_, func
from models import Memo, MemoDt, MemoAttachment
from common.generator import generate_code
from common.enum import CodeCounterEnum
from schemas.memo_sch import MemoCreateSch, MemoUpdateSch
from schemas.oauth import AccessToken
import crud

class CRUDMemo(CRUDBase[Memo, MemoCreateSch, MemoUpdateSch]):
    async def get_by_id(self, *, id:str) -> Memo:

        query = select(Memo)
        query = query.where(Memo.id == id)
        query = query.options(selectinload(Memo.project), selectinload(Memo.company))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
    async def create_memo_w_detail(self, *, sch:MemoCreateSch, created_by:str) -> Memo:
        
        sch.no_memo = await generate_code(entity=CodeCounterEnum.MEMO)

        db_memo = Memo.model_validate(sch)

        if created_by:
            db_memo.created_by = db_memo.updated_by = created_by

        db.session.add(db_memo)

        for detail in sch.memo_details:
            db_detail = MemoDt(doc_type_id=detail.doc_type_id, 
                                  unit_id=detail.unit_id, 
                                  nomor=detail.nomor, 
                                  name=detail.name,
                                  company_id=detail.company_id, 
                                  tanggal=detail.tanggal, 
                                  alashak_id=detail.alashak_id, 
                                  tipe_doc_fisik=detail.tipe_doc_fisik, 
                                  remarks=detail.remarks,
                                  created_by=created_by,
                                  updated_by=created_by)
            db.session.add(db_detail)

            for attachment in detail.attachments:
                db_attachment = MemoAttachment(memo_dt_id=db_detail.id, file_path=attachment.file_path, created_by=created_by, updated_by=created_by)
                db.session.add(db_attachment)

        await db.session.commit()
        return db_memo
    
    # async def update_and_mapping_w_doc_detail(self, *, obj_current:Memo, obj_new:MemoUpdateSch, updated_by:str) -> Memo:

    #     obj_data = jsonable_encoder(obj_current)
    #     update_data = obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)

    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(obj_current, field, update_data[field])
    #         elif updated_by and updated_by != "" and field == "updated_by":
    #             setattr(obj_current, field, updated_by)

    #     db.session.add(obj_current)
    #     await db.session.flush()

    #     current_doc_detail = await crud.doc_detail.get_by_doc_type(doc_type_id=obj_current.id)

    #     for dt in obj_new.doc_archives:
    #         current_doc_type_archive = await crud.doc_type_archive.get_doc_type_archive(doc_type_id=obj_current.id, doc_format_id=dt.id, jenis_arsip=dt.jenis_arsip)

    #         if not current_doc_type_archive:
    #             doc_format = await crud.doc_format.get(id=dt.id)
    #             if not doc_format:
    #                 raise HTTPException(status_code=404, detail=f"Document format not found!")

    #             db_obj_map_archive = DocTypeArchive(doc_format_id=dt.id, doc_type_id=obj_current.id, jenis_arsip=dt.jenis_arsip)
    #             db.session.add(db_obj_map_archive)
    #         else:
    #             current_doc_type_archives.remove(current_doc_type_archive)

    #     for remove in current_doc_type_archives:
    #         await db.session.delete(remove)

    #     await db.session.commit()
    #     await db.session.refresh(obj_current)

    #     return obj_current

    async def get_paginated(self, *, params: Params | None = Params(), **kwargs):
        query = self.base_query()
        query = self.create_filter(query=query, filter=kwargs)

        return await paginate(db.session, query, params)
    
    def base_query(self):
        
        query = select(Memo)
        query = query.options(selectinload(Memo.project), selectinload(Memo.company))
        
        return query

    def create_filter(self, *, query, filter:dict):

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
