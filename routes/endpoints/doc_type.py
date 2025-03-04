from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from fastapi_pagination import Params
from schemas.response_sch import PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response
from schemas.doc_type_sch import (DocTypeSch, DocTypeUpdateSch, DocTypeCreateSch, DocTypeByIdSch)
from schemas.doc_type_column_sch import DocTypeColumnCreateUpdateSch
from models.doc_type_model import DocType
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocTypeSch])
async def get_list(params: Params=Depends()):

    query = select(DocType)

    objs = await crud.doc_type.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocTypeSch]])
async def get_no_page():

    query = select(DocType)

    objs = await crud.doc_type.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DocTypeByIdSch])
async def get_by_id(id: str):

    obj = await crud.doc_type.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(DocType, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DocTypeSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DocTypeCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user

    obj = await crud.doc_type.create_doc_type_and_mapping(sch=sch, created_by=login_user.client_id)

    doc_type = await crud.doc_type.get_by_id(id=obj.id)

    return create_response(data=doc_type)

@router.put("/{id}", response_model=PostResponseBaseSch[DocTypeByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DocTypeUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.doc_type.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type tidak ditemukan")

    obj_updated = await crud.doc_type.update_doc_type_and_mapping(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.doc_type.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)

@router.put("/mapping/jenis-kolom", response_model=PostResponseBaseSch[DocTypeSch], status_code=status.HTTP_201_CREATED)
async def mapping_doctype_jeniskolom(request: Request, sch: DocTypeColumnCreateUpdateSch):
    
    """Create a new object"""

    obj = await crud.doc_type_column_type.mapping_doc_type_jenis_kolom(sch=sch)
    doc_type = await crud.doc_type.get_by_id(id=obj)
    return create_response(data=doc_type)




