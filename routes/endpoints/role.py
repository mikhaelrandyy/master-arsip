from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_, String, cast
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.role_sch import (RoleSch, RoleUpdateSch, RoleCreateSch, RoleByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.role_model import Role
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[RoleSch])
async def get_list(search:str | None = None, params: Params=Depends()):

    query = select(Role)

    objs = await crud.role.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[RoleSch]])
async def get_no_page():

    query = select(Role)

    objs = await crud.role.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[RoleByIdSch])
async def get_by_id(id: str):

    obj = await crud.role.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(Role, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[RoleSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: RoleCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.role.create(obj_in=sch, created_by=login_user.client_id)

    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[RoleByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: RoleUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.role.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type Group tidak ditemukan")

    obj_updated = await crud.role.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)

    response_obj = await crud.role.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





