from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.oauth import AccessToken
from schemas.department_sch import (DepartmentSch, DepartmentUpdateSch, DepartmentCreateSch, DepartmentByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.department_model import Department
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DepartmentSch])
async def get_list(
    request: Request,
    params: Params=Depends(),
    search: str | None = None,
    order_by: str | None = None
):
    login_user: AccessToken = request.state.login_user
    objs = await crud.department.get_paginated(params=params, login_user=login_user, search=search, order_by=order_by)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DepartmentSch]])
async def get_no_page(
    request: Request,
    search: str | None = None,
    order_by: str | None = None
):
    login_user: AccessToken = request.state.login_user
    objs = await crud.department.get_no_page(login_user=login_user, search=search, order_by=order_by)

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DepartmentByIdSch])
async def get_by_id(id: str):

    obj = await crud.department.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(Department, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DepartmentSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DepartmentCreateSch):
    
    """Create a new object"""
    login_user: AccessToken = request.state.login_user
    obj = await crud.department.create(obj_in=sch, created_by=login_user.client_id)
    response_obj = await crud.department.get_by_id(id=obj.id)
    return create_response(data=response_obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DepartmentSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DepartmentUpdateSch):
    
    login_user:AccessToken = request.state.login_user
    obj_current = await crud.department.get(id=id)

    if not obj_current:
        raise IdNotFoundException(Department, id)

    obj_updated = await crud.department.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.department.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)

@router.post("/mapping/doc-type/{id}", response_model=PostResponseBaseSch[DepartmentSch], status_code=status.HTTP_201_CREATED)
async def mapping_department_doc_type(id:str, doc_type_ids: list[str]):
    
    """Create a new mapping with doc type"""

    obj_current = await crud.department.get(id=id)
    if not obj_current:
        raise IdNotFoundException(Department, id)
    
    await crud.department.update_and_mapping_w_doc_type(obj_current=obj_current, doc_type_ids=doc_type_ids)
    response_obj = await crud.department.get_by_id(id=obj_current.id)

    return create_response(data=response_obj)




