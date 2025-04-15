from fastapi import APIRouter, HTTPException, Request
from fastapi_async_sqlalchemy import db
import crud.workflow_crud
from schemas.workflow_sch import WorkflowSystemCallbackSch, WorkflowUpdateSch, WorkflowCreateSch
from schemas.workflow_history_sch import WorkflowHistoryCreateSch
from schemas.workflow_next_approver_sch import WorkflowNextApproverCreateSch
from services.helper_service import HelperService
from services.signature_service import SignatureService
from services.gcloud_task_service import GCloudTaskService
from configs.config import settings
from common.enum import WorkflowLastStatusEnum, WorkflowEntityEnum
import crud
import json

router = APIRouter()

@router.post("/notification")
async def notification(payload: dict, request:Request):
    
    """Notification Workflow"""
    try:
        # signature = request.headers.get("Signature", None)
        # verify = SignatureService().verify_signature_request(msg=payload, signature=signature, client_public_key=settings.WF_PUBLIC_KEY)

        # if verify == False:
        #     raise HTTPException(status_code=401, detail="Signature not authorize!")
        
        await crud.workflow.notification(payload=payload, request=request)

        return {"success" : True}
    
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))