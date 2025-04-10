from fastapi import APIRouter, status, HTTPException, Request, Depends
from fastapi_pagination import Params
from schemas.desa_sch import (DesaSch, DesaUpdateSch, DesaCreateSch, DesaByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from schemas.common_sch import OrderEnumSch
from models.desa_model import Desa
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DesaSch])
async def get_list(
    search:str | None = None, 
    order_by: str | None = "created_at",
    order: OrderEnumSch | None = OrderEnumSch.descendent,
    params: Params=Depends()
):

    objs = await crud.desa.get_paginated(search=search, params=params, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DesaSch]])
async def get_no_page(
    search: str | None = None,
    order_by: str | None = "created_at",
    order: OrderEnumSch | None = OrderEnumSch.descendent
):

    objs = await crud.desa.get_no_paginated(search=search, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DesaByIdSch])
async def get_by_id(id: str):

    obj = await crud.desa.get_by_id(id=id)
    if obj is None:
        raise IdNotFoundException(Desa, id)
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DesaSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DesaCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.desa.create(obj_in=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DesaByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DesaUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.desa.get(id=id)
    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Desa tidak ditemukan")
    obj_updated = await crud.desa.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.desa.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





