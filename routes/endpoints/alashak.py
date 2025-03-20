from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.common_sch import OrderEnumSch
from schemas.alashak_sch import (AlashakSch, AlashakUpdateSch, AlashakCreateSch, AlashakByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.alashak_model import Alashak
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[AlashakSch])
async def get_list(
    search: str | None = None,
    order_by: str | None = "created_at", 
    order: OrderEnumSch | None = OrderEnumSch.descendent,
    params: Params=Depends()
):
    objs = await crud.alashak.get_paginated(search=search, params=params, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[AlashakSch]])
async def get_no_page(
    search: str | None = None,
    order_by: str | None = "created_at",
    order: OrderEnumSch | None = OrderEnumSch.descendent
):

    objs = await crud.alashak.get_no_paginated(search=search, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[AlashakByIdSch])
async def get_by_id(id: str):

    obj = await crud.alashak.get(id=id)
    if obj is None:
        raise IdNotFoundException(Alashak, id)
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[AlashakSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: AlashakCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.alashak.create(obj_in=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[AlashakByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: AlashakUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user
    obj_current = await crud.alashak.get(id=id)
    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Alashak tidak ditemukan")
    obj_updated = await crud.alashak.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.alashak.get(id=obj_updated.id)
    return create_response(data=response_obj)





