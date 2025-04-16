from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_, cast, String
from fastapi_pagination import Params
from models import (
    DocType, 
    DocTypeGroup
)
from schemas.oauth import AccessToken
from schemas.response_sch import PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response
from schemas.doc_type_sch import (DocTypeSch, DocTypeUpdateSch, DocTypeCreateSch, DocTypeByIdSch)
from schemas.doc_type_column_sch import DocTypeColumnCreateUpdateSch
from schemas.common_sch import OrderEnumSch
from common.enum import JenisArsipEnum
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocTypeSch])
async def get_list(
    request: Request, 
    search: str | None = None, 
    order_by: str | None = "created_at", 
    order: OrderEnumSch | None = OrderEnumSch.descendent,
    params: Params=Depends(), 
    jenis_arsip:JenisArsipEnum | None = None):

    login_user: AccessToken = request.state.login_user
    objs = await crud.doc_type.get_paginated(login_user=login_user, params=params, search=search, jenis_arsip=jenis_arsip, order_by=order_by, order=order)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocTypeSch]])
async def get_no_page(
    request: Request, 
    search: str | None = None, 
    order_by: str | None = "created_at", 
    order: OrderEnumSch | None = OrderEnumSch.descendent,
    jenis_arsip:JenisArsipEnum | None = None):

    login_user : AccessToken = request.state.login_user
    objs = await crud.doc_type.get_no_paginated(search=search, order_by=order_by, order=order, jenis_arsip=jenis_arsip, login_user=login_user)
    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DocTypeByIdSch])
async def get_by_id(id: str):

    obj = await crud.doc_type.get_by_id(id=id)
    if obj is None:
        raise IdNotFoundException(DocType, id)
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DocTypeSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DocTypeCreateSch):
    
    """Create a new object"""

    login_user : AccessToken = request.state.login_user

    if sch.code:
        obj_code_exists = await crud.doc_type.get_by_code_upper(code=sch.code)
        if obj_code_exists:
            raise HTTPException(status_code=400, detail="Document Type dengan code yang sama sudah eksis")
    
    obj_name_exists = await crud.doc_type.get_by_name_upper(name=sch.name)
    if obj_name_exists:
        raise HTTPException(status_code=400, detail="Document Type dengan nama yang sama sudah eksis")

    obj = await crud.doc_type.create_and_mapping_w_doc_format_column(sch=sch, created_by=login_user.client_id)
    response_obj = await crud.doc_type.get_by_id(id=obj.id)
    return create_response(data=response_obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DocTypeSch], status_code=status.HTTP_201_CREATED)
async def update(request: Request, id: str, sch: DocTypeUpdateSch):
    
    login_user : AccessToken = request.state.login_user

    obj_code_exists = await crud.doc_type.get_by_code_upper(code=sch.code)
    if obj_code_exists and obj_code_exists.id != id:
        raise HTTPException(status_code=400, detail="Document Type dengan code yang sama sudah eksis")
    
    obj_name_exists = await crud.doc_type.get_by_name_upper(name=sch.name)
    if obj_name_exists and obj_name_exists.id != id:
        raise HTTPException(status_code=400, detail="Document Type dengan nama yang sama sudah eksis")

    obj_current = await crud.doc_type.get(id=id)
    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type tidak ditemukan")
    obj_updated = await crud.doc_type.update_and_mapping_w_doc_format_column(obj_current=obj_current, obj_new=sch, updated_by=login_user.client_id)
    response_obj = await crud.doc_type.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)