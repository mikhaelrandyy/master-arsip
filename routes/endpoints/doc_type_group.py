from fastapi import APIRouter, status, HTTPException, Request, Depends
from fastapi_pagination import Params
from sqlmodel import select
from schemas.common_sch import OrderEnumSch
from schemas.doc_type_group_sch import (DocTypeGroupSch, DocTypeGroupUpdateSch, DocTypeGroupCreateSch, DocTypeGroupByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.doc_type_group_model import DocTypeGroup
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocTypeGroupSch])
async def get_list(
    search: str | None = None, 
    order_by: str | None = "created_at",
    order: OrderEnumSch | None = OrderEnumSch.descendent,
    params: Params=Depends()):

    objs = await crud.doc_type_group.get_paginated(params=params, search=search, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocTypeGroupSch]])
async def get_no_page(
    search: str | None = None,
    order_by: str | None = "created_at",
    order: OrderEnumSch | None = OrderEnumSch.descendent
):
    objs = await crud.doc_type_group.get_no_paginated(search=search, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DocTypeGroupByIdSch])
async def get_by_id(id: str):

    obj = await crud.doc_type_group.get_by_id(id=id)
    if obj is None:
        raise IdNotFoundException(DocTypeGroup, id)
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DocTypeGroupSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DocTypeGroupCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.doc_type_group.create(sch=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DocTypeGroupByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DocTypeGroupUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user
    obj_current = await crud.doc_type_group.get(id=id)
    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type Group tidak ditemukan")
    obj_updated = await crud.doc_type_group.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.doc_type_group.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





