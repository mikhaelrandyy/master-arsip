from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.departement_sch import (DepartementSch, DepartementUpdateSch, DepartementCreateSch, DepartementByIdSch, DepartementCreateForMappingSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.departement_model import Departement
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DepartementSch])
async def get_list(params: Params=Depends()):

    query = select(Departement)

    objs = await crud.departement.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DepartementSch]])
async def get_no_page():

    query = select(Departement)

    objs = await crud.departement.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DepartementByIdSch])
async def get_by_id(id: str):

    obj = await crud.departement.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(Departement, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DepartementSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DepartementCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.departement.create(obj_in=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DepartementByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DepartementUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.departement.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Data tidak tersedia")

    obj_updated = await crud.departement.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)

    response_obj = await crud.departement.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)


@router.post("/mapping/doc-type", response_model=PostResponseBaseSch[DepartementSch], status_code=status.HTTP_201_CREATED)
async def create_mapping(request: Request, sch: DepartementCreateForMappingSch):
    
    """Create a new object"""
    
    obj = await crud.departement.create_dept_mapping(sch=sch)

    return create_response(data=obj)




