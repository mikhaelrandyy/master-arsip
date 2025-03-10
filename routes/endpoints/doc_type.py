from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_, cast, String
from fastapi_pagination import Params
from schemas.oauth import AccessToken
from schemas.response_sch import PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response
from schemas.doc_type_sch import (DocTypeSch, DocTypeUpdateSch, DocTypeCreateSch, DocTypeByIdSch)
from schemas.doc_type_column_sch import DocTypeColumnCreateUpdateSch
from models.doc_type_model import DocType
from models import DocTypeGroup
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocTypeSch])
async def get_list(request: Request, search: str | None = None, order_by: str | None = None, params: Params=Depends()):

    login_user: AccessToken = request.state.login_user
    objs = await crud.doc_type.get_paginated(search=search, order_by=order_by, params=params, login_user=login_user)
    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocTypeSch]])
async def get_no_page(request: Request, search: str | None = None, order_by: str | None = None,):

    login_user : AccessToken = request.state.login_user
    objs = await crud.doc_type.get_no_page(login_user=login_user, search=search, order_by=order_by)

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
    obj = await crud.doc_type.create_and_mapping_w_doc_format(sch=sch, created_by=login_user.client_id)
    response_obj = await crud.doc_type.get_by_id(id=obj.id)

    return create_response(data=response_obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DocTypeSch], status_code=status.HTTP_201_CREATED)
async def update(request: Request, id: str, obj_new: DocTypeUpdateSch):
    
    login_user : AccessToken = request.state.login_user
    obj_current = await crud.doc_type.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type tidak ditemukan")

    obj_updated = await crud.doc_type.update_and_mapping_w_doc_format(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.doc_type.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)

@router.post("/mapping/column_type/{id}", response_model=PostResponseBaseSch[DocTypeSch], status_code=status.HTTP_201_CREATED)
async def mapping_doc_type_column(request: Request, id:str, column_type_ids: list[str]):
    
    """Create a new Mapping"""

    obj_current = await crud.doc_type.get(id=id)
    if not obj_current:
        raise IdNotFoundException(DocType, id=id)

    await crud.doc_type.update_and_mapping_w_column_type(obj_current=obj_current, column_type_ids=column_type_ids)

    response_obj = await crud.doc_type.get_by_id(id=obj_current.id)
    return create_response(data=response_obj)



