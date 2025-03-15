from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_, String, cast
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.oauth import AccessToken
from schemas.memo_sch import (MemoSch, MemoUpdateSch, MemoCreateSch, MemoByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.memo_model import Memo
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[MemoSch])
async def get_list(request: Request, search:str | None = None, order_by: str | None = None, params: Params=Depends()):

    # login_user: AccessToken = request.state.login_user
    objs = await crud.memo.get_paginated(search=search, order_by=order_by, params=params)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[MemoSch]])
async def get_no_page():

    query = select(Memo)

    objs = await crud.memo.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[MemoByIdSch])
async def get_by_id(id: str):

    obj = await crud.memo.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(Memo, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[MemoSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: MemoCreateSch):
    
    """Create a new object"""
    login_user: AccessToken = request.state.login_user
    obj = await crud.memo.create(memo=sch, created_by=login_user.client_id)
    response_obj = await crud.memo.get_by_id(id=obj.id)
    return create_response(data=response_obj)

@router.put("/{id}", response_model=PostResponseBaseSch[MemoSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: MemoUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.memo.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Memo tidak ditemukan")

    obj_updated = await crud.memo.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)

    response_obj = await crud.memo.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





