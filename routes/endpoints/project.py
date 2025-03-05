from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_, String, cast
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.project_sch import (ProjectSch, ProjectUpdateSch, ProjectCreateSch, ProjectByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.project_model import Project
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[ProjectSch])
async def get_list(search:str | None = None, params: Params=Depends()):

    query = select(Project)

    objs = await crud.project.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[ProjectSch]])
async def get_no_page():

    query = select(Project)

    objs = await crud.project.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[ProjectByIdSch])
async def get_by_id(id: str):

    obj = await crud.project.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(Project, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[ProjectSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: ProjectCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.project.create(obj_in=sch, created_by=login_user.client_id)

    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[ProjectByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: ProjectUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.project.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Project tidak ditemukan")

    obj_updated = await crud.project.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)

    response_obj = await crud.Project.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





