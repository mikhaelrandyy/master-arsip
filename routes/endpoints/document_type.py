from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from sqlalchemy.orm import selectinload
from fastapi_pagination import Params
from schemas.document_type_sch import (DocumentTypeSch, DocumentTypeUpdateSch, DocumentTypeCreateSch, DocumentTypeByIdSch)
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
from models.document_type_model import DocumentType
import crud
from utils.exceptions.common_exception import IdNotFoundException

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[DocumentTypeSch])
async def get_list(params: Params=Depends()):

    query = select(DocumentType)

    objs = await crud.document_type.get_multi_paginated_ordered(query=query, params=params)

    return create_response(data=objs)

@router.get("/no-page", response_model=GetResponseBaseSch[list[DocumentTypeSch]])
async def get_no_page():

    query = select(DocumentType)

    objs = await crud.document_type.get_all_ordered(query=query, order_by="created_at")

    return create_response(data=objs)

@router.get("/{id}", response_model=GetResponseBaseSch[DocumentTypeByIdSch])
async def get_by_id(id: str):

    obj = await crud.document_type.get_by_id(id=id)

    if obj is None:
        raise IdNotFoundException(DocumentType, id)
    
    return create_response(data=obj)

@router.post("", response_model=PostResponseBaseSch[DocumentTypeSch], status_code=status.HTTP_201_CREATED)
async def create(request: Request, sch: DocumentTypeCreateSch):
    
    """Create a new object"""
    if hasattr(request.state, 'login_user'):
        login_user=request.state.login_user

    obj = await crud.document_type.create_doc_type_and_mapping(sch=sch, created_by=login_user.client_id)
    return create_response(data=obj)

@router.put("/{id}", response_model=PostResponseBaseSch[DocumentTypeByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DocumentTypeUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.document_type.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type tidak ditemukan")

    obj_updated = await crud.document_type.update(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.document_type.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)





