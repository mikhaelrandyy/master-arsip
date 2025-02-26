from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.doc_format_jenis_arsip_doc_type_link_sch import (DocFormatJenisArsipDocTypeLinkSch, DocFormatJenisArsipDocTypeLinkUpdateSch, DocFormatJenisArsipDocTypeLinkCreateSch, DocFormatJenisArsipDocTypeLinkByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.doc_format_jenis_arsip_doc_type_model import DocFormatJenisArsipDocTypeLink
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocFormatJenisArsipDocTypeLinkSch])
async def get_list(params: Params=Depends()):

    query = select(DocFormatJenisArsipDocTypeLink)

    objs = await crud.doc_format_jenis_arsip__doc_type_link.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocFormatJenisArsipDocTypeLinkSch]])
async def get_no_page():

    query = select(DocFormatJenisArsipDocTypeLink)

    objs = await crud.doc_format_jenis_arsip__doc_type_link.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DocFormatJenisArsipDocTypeLinkByIdSch])
async def get_by_id(id: str):

    obj = await crud.doc_format_jenis_arsip__doc_type_link.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(DocFormatJenisArsipDocTypeLink, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DocFormatJenisArsipDocTypeLinkSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DocFormatJenisArsipDocTypeLinkCreateSch):
    
    """Create a new object"""
    obj = await crud.doc_format_jenis_arsip__doc_type_link.create(obj_in=sch)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DocFormatJenisArsipDocTypeLinkByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DocFormatJenisArsipDocTypeLinkUpdateSch):
    
    obj_current = await crud.doc_format_jenis_arsip__doc_type_link.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Data tidak ditemukan")

    obj_updated = await crud.doc_format_jenis_arsip__doc_type_link.update(obj_current=obj_current, obj_new=obj_new)
    response_obj = await crud.doc_format_jenis_arsip__doc_type_link.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





