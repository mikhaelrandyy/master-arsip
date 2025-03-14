from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_, String, cast
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.worker_sch import (WorkerSch, WorkerUpdateSch, WorkerCreateSch, WorkerByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.worker_model import Worker
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[WorkerSch])
async def get_list(search:str | None = None, params: Params=Depends()):

    query = select(Worker)

    if search:
        query = query.filter(
                or_(
                    cast(Worker.client_id, String).ilike(f'%{search}%'),
                    cast(Worker.is_active, String).ilike(f'%{search}%')
                )
            )

    objs = await crud.worker.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[WorkerSch]])
async def get_no_page():

    query = select(Worker)

    objs = await crud.worker.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[WorkerByIdSch])
async def get_by_id(id: str):

    obj = await crud.worker.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(Worker, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[WorkerSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: WorkerCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user
    obj = await crud.worker.create(sch=sch, created_by=login_user.client_id)
    worker = await crud.worker.get_by_id(id=obj.id)
    return create_response(data=worker)

@router.put("/{id}", response_model=PostResponseBaseSch[WorkerByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: WorkerUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.worker.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Worker tidak ditemukan")

    obj_updated = await crud.worker.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)

    response_obj = await crud.worker.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





