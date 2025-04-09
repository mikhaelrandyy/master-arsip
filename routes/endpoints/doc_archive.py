from fastapi import APIRouter, status, HTTPException, Request, Depends, Body
import crud.doc_archive_crud
from schemas.doc_archive_sch import DocArchiveSch
from schemas.response_sch import (PostResponseBaseSch, GetResponseBaseSch, GetResponsePaginatedSch, create_response)
import crud

router = APIRouter()

@router.post("/task_create", response_model=PostResponseBaseSch[DocArchiveSch], status_code=status.HTTP_201_CREATED)
async def create(memo_id: str):
    
    """Create a new object"""
    # if hasattr(request.state, 'login_user'):
        # login_user=request.state.login_user
    obj = await crud.doc_archive.create_doc_archive(memo_id=memo_id)
    return create_response(data=obj)

@router.post("/task/notif-from-memo")
async def notif_from_memo(request: dict = Body(..., example={"memo_id": "string"})):
    """Receive notification from memo"""
    await crud.doc_archive.notif_from_memo(request)
    return create_response({"MESSAGE" : "SUCCESSFULLY"})





