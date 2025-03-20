from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.common_sch import OrderEnumSch
from schemas.doc_format_sch import (DocFormatSch, DocFormatUpdateSch, DocFormatCreateSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.doc_format_model import DocFormat
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocFormatSch])
async def get_list(
    search:str | None = None, 
    params: Params=Depends(),
    order_by: str | None = "created_at",
    order: OrderEnumSch | None = OrderEnumSch.descendent
    ):

    objs = await crud.doc_format.get_paginated(params=params, search=search, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocFormatSch]])
async def get_no_page(
    search:str | None = None,
    order_by: str | None = "created_at",
    order: OrderEnumSch | None = OrderEnumSch.descendent
    ):

    objs = await crud.doc_format.get_no_paginated(search=search, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DocFormatSch])
async def get_by_id(id: str):

    obj = await crud.doc_format.get(id=id)
    if obj is None:
        raise IdNotFoundException(DocFormat, id)
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DocFormatSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DocFormatCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.doc_format.create(sch=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DocFormatSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DocFormatUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user
    obj_current = await crud.doc_format.get(id=id)
    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Format tidak ditemukan")
    obj_updated = await crud.doc_format.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    return create_response(data=obj_updated)





