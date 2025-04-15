from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_, cast, String
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.oauth import AccessToken
from schemas.common_sch import OrderEnumSch
from schemas.column_type_sch import (ColumnTypeSch, ColumnTypeUpdateSch, ColumnTypeCreateSch, ColumnTypeByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.column_type_model import ColumnType
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[ColumnTypeSch])
async def get_list(
    search: str | None = None, 
    order_by:str | None = "created_at", 
    order: OrderEnumSch | None = OrderEnumSch.descendent, 
    params: Params=Depends()):

    objs = await crud.column_type.get_paginated(search=search, params=params, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[ColumnTypeSch]])
async def get_no_page(
    search: str | None = None,
    order_by: str | None = "created_at", 
    order: OrderEnumSch | None = OrderEnumSch.descendent):

    objs = await crud.column_type.get_no_paginated(search=search, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[ColumnTypeByIdSch])
async def get_by_id(id: str):

    obj = await crud.column_type.get_by_id(id=id)
    if obj is None:
        raise IdNotFoundException(ColumnType, id)
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[ColumnTypeSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: ColumnTypeCreateSch):
    
    """Create a new object"""
    login_user : AccessToken = request.state.login_user
    obj = await crud.column_type.create(sch=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[ColumnTypeByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: ColumnTypeUpdateSch):

    login_user : AccessToken = request.state.login_user
    obj_current = await crud.column_type.get(id=id)
    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Jenis Kolom tidak ditemukan")
    obj_updated = await crud.column_type.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.column_type.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





