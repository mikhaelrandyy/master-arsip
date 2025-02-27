from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.doc_type_jenis_kolom_link_sch import DocTypeJenisKolomLinkSch, DocTypeJenisKolomLinkUpdateSch, DocTypeJenisKolomLinkForMappingSch, DocTypeJenisKolomLinkByIdSch
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.doc_type_jenis_kolom_model import DocTypeJenisKolomLink
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocTypeJenisKolomLinkSch])
async def get_list(params: Params=Depends()):

    query = select(DocTypeJenisKolomLink)

    objs = await crud.doc_type_jenis_kolom_link.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocTypeJenisKolomLinkSch]])
async def get_no_page():

    query = select(DocTypeJenisKolomLink)

    objs = await crud.doc_type_jenis_kolom_link.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DocTypeJenisKolomLinkByIdSch])
async def get_by_id(id: str):

    obj = await crud.doc_type_jenis_kolom_link.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(DocTypeJenisKolomLink, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DocTypeJenisKolomLinkForMappingSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DocTypeJenisKolomLinkForMappingSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user

    obj = await crud.doc_type_jenis_kolom_link.create_mapping(sch=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DocTypeJenisKolomLinkByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DocTypeJenisKolomLinkUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.doc_type_jenis_kolom_link.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type tidak ditemukan")

    obj_updated = await crud.doc_type_jenis_kolom_link.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.doc_type_jenis_kolom_link.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





