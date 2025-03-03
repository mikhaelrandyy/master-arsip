from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlmodel import select, or_
from fastapi_pagination import Params
from schemas.response_sch import PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response
from schemas.document_type_sch import (DocumentTypeSch, DocumentTypeUpdateSch, DocumentTypeCreateSch, DocumentTypeByIdSch)
from schemas.doc_type_jenis_kolom_sch import DocTypeJenisKolomForMappingSch, DocTypeJenisKolomByIdSch, DocTypeJenisKolomUpdateSch
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

    doc_type = await crud.document_type.get_by_id(id=obj.id)

    return create_response(data=doc_type)

@router.put("/{id}", response_model=PostResponseBaseSch[DocumentTypeByIdSch], status_code=status.HTTP_201_CREATED)
async def update(id: str, request: Request, obj_new: DocumentTypeUpdateSch):
    
    if hasattr(request.state, 'login_user'):
        login_user = request.state.login_user

    obj_current = await crud.document_type.get(id=id)

    if not obj_current:
        raise HTTPException(status_code=404, detail=f"Document Type tidak ditemukan")

    obj_updated = await crud.document_type.update_doc_type_and_mapping(obj_current=obj_current, obj_new=obj_new, updated_by=login_user.client_id)
    response_obj = await crud.document_type.get_by_id(id=obj_updated.id)
    return create_response(data=response_obj)

@router.post("/mapping/jenis-kolom", response_model=PostResponseBaseSch[DocumentTypeSch], status_code=status.HTTP_201_CREATED)
async def create_mapping_doctype_jeniskolom(request: Request, sch: DocTypeJenisKolomForMappingSch):
    
    """Create a new object"""

    obj = await crud.doc_type_jenis_kolom.create_mapping_doc_type_jenis_kolom(sch=sch)
    doc_type = await crud.document_type.get_by_id(id=obj)
    return create_response(data=doc_type)

@router.put("/mapping/jenis-kolom", response_model=PostResponseBaseSch[DocumentTypeSch], status_code=status.HTTP_201_CREATED)
async def update_mapping_doctype_jeniskolom(obj_new: DocTypeJenisKolomForMappingSch):
    
    obj_updated = await crud.doc_type_jenis_kolom.update_mapping_doc_type_jenis_kolom(obj_new=obj_new)
    doc_type = await crud.document_type.get_by_id(id=obj_updated)
    return create_response(data=doc_type)




