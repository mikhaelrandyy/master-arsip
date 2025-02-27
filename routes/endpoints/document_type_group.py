from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.document_type_group_sch import (DocumentTypeGroupSch, DocumentTypeGroupUpdateSch, DocumentTypeGroupCreateSch, DocumentTypeGroupByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.document_type_group_model import DocumentTypeGroup
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocumentTypeGroupSch])
async def get_list(params: Params=Depends()):

    query = select(DocumentTypeGroup)

    objs = await crud.document_type_group.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocumentTypeGroupSch]])
async def get_no_page():

    query = select(DocumentTypeGroup)

    objs = await crud.document_type_group.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DocumentTypeGroupByIdSch])
async def get_by_id(id: str):

    obj = await crud.document_type_group.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(DocumentTypeGroup, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DocumentTypeGroupSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DocumentTypeGroupCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.document_type_group.create(obj_in=sch, created_by=login_user.id)

    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DocumentTypeGroupByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DocumentTypeGroupUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.document_type_group.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type Group tidak ditemukan")

    obj_updated = await crud.document_type_group.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.id)
    response_obj = await crud.document_type_group.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





