# from fastapi import APIRouter, status, HTTPException, Request, Depends
# from sqlmodel import select, or_
# from sqlalchemy.orm import selectinload
# from fastapi_pagination import Params
# from schemas.document_type_sch import (AlashakSch, AlashakCreateSch, AlashakByIdSch)
# from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
# from models.document_type_model import Alashak
# import crud
# from utils.exceptions.common_exception import IdNotFoundException

# router = APIRouter()

# @router.get("", response_model=GetResponsePaginatedSch[AlashakSch])
# async def get_list(params: Params=Depends()):

#     query = select(Alashak)

#     objs = await crud.document_type.get_multi_paginated_ordered(query=query, params=params)

#     return create_response(data=objs)

# @router.post("", response_model=PostResponseBaseSch[list[AlashakSch]], status_code=status.HTTP_201_CREATED)
# async def create(request: Request, sch: AlashakCreateSch):
    
#     """Create a new object"""
#     if hasattr(request.state, 'login_user'):
#         login_user=request.state.login_user
#     obj = await crud.document_type.create(sch=sch, created_by=login_user.client_id)
#     return create_response(data=obj)


