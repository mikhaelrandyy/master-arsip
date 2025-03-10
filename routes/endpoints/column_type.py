from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_, cast, String
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.column_type_sch import (ColumnTypeSch, ColumnTypeUpdateSch, ColumnTypeCreateSch, ColumnTypeByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.column_type_model import ColumnType
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[ColumnTypeSch])
async def get_list(search: str | None = None, params: Params=Depends()):

    query = select(ColumnType)

    if search:
        query = query.filter(
                or_(
                    cast(ColumnType.name, String).ilike(f'%{search}%'),
                    cast(ColumnType.tipe_data, String).ilike(f'%{search}%')
                )
            )

    objs = await crud.column_type.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[ColumnTypeSch]])
async def get_no_page():

    query = select(ColumnType)

    objs = await crud.column_type.get_all_ordered(query=query, order_by="created_at")

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
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user

    obj = await crud.column_type.create(sch=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[ColumnTypeByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: ColumnTypeUpdateSch):

    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    
    obj_current = await crud.column_type.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Jenis Kolom tidak ditemukan")

    obj_updated = await crud.column_type.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.column_type.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





