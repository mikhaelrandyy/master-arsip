from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select
from common.enum import WorkflowEntityEnum
from crud.base_crud import CRUDBase
from models.workflow_model import Workflow
from common.enum import WorkflowLastStatusEnum, WorkflowEntityEnum
from schemas.workflow_sch import WorkflowSystemCallbackSch, WorkflowUpdateSch, WorkflowCreateSch
from schemas.workflow_history_sch import WorkflowHistoryCreateSch
from schemas.workflow_next_approver_sch import WorkflowNextApproverCreateSch
from services.helper_service import HelperService
from services.gcloud_task_service import GCloudTaskService
import crud

class CRUDWorkflow(CRUDBase[Workflow, WorkflowCreateSch, WorkflowUpdateSch]):
    async def get_by_reference_id(self, 
                  *, 
                  reference_id: str | None = None,
                  query : Workflow | Select[Workflow] | None = None
                  ) -> Workflow | None:
        
        if query == None:
            query = select(self.model).where(self.model.reference_id == reference_id)

        response = await db.session.execute(query)

        return response.scalar_one_or_none()
    
    async def notification(self, payload, request):

        sch = WorkflowSystemCallbackSch(**payload)

        obj_current = await crud.workflow.get_by_reference_id(reference_id=sch.client_reff_no)
        if obj_current is None:
            raise HTTPException(status_code=422, detail="Client Reff No not found")
        
        await crud.workflow_next_approver.delete_by_workflow_id(workflow_id=obj_current.id, with_commit=False)
        
        obj_new = WorkflowUpdateSch(reference_id=obj_current.reference_id,
                                    txn_id=sch.txn_id,
                                    entity=obj_current.entity, 
                                    flow_id=obj_current.flow_id,
                                    step_name=sch.step_name,
                                    last_status=sch.last_status_enum,
                                    last_status_at=HelperService().no_timezone(sch.last_status_at),
                                    last_step_app_email= sch.last_step_approver.email if sch.last_step_approver else None,
                                    last_step_app_name=sch.last_step_approver.name if sch.last_step_approver else None,
                                    last_step_app_action=sch.last_step_approver.status if sch.last_step_approver else None,
                                    last_step_app_action_at=HelperService().no_timezone(sch.last_step_approver.confirm_at) if sch.last_step_approver else None,
                                    last_step_app_action_remarks=sch.last_step_approver.confirm_remarks if sch.last_step_approver else None,
                                    version=obj_current.version
                                    )

        obj_updated = await crud.workflow.update(obj_current=obj_current, obj_new=obj_new, with_commit=False)

        await self.create_next_approver(sch=sch, obj_updated=obj_updated)

        await self.create_history(sch=sch, obj_updated=obj_updated, request=request)


    async def create_next_approver(self, sch:WorkflowSystemCallbackSch, obj_updated:Workflow):

        if sch.next_approver is not None:
              for next_approver in sch.next_approver:
                  obj_next_approver_new = WorkflowNextApproverCreateSch(**next_approver.model_dump(), workflow_id=obj_updated.id)
                  await crud.workflow_next_approver.create(obj_in=obj_next_approver_new, created_by=obj_updated.created_by, with_commit=False)


    async def create_history(self, sch:WorkflowSystemCallbackSch, obj_updated:Workflow, request):

        obj_in = WorkflowHistoryCreateSch(
                                        workflow_id=obj_updated.id,
                                        step_name=sch.step_name,
                                        last_status=sch.last_status_enum,
                                        last_status_at=HelperService().no_timezone(sch.last_status_at),
                                        last_step_app_email= sch.last_step_approver.email if sch.last_step_approver else None,
                                        last_step_app_name=sch.last_step_approver.name if sch.last_step_approver else None,
                                        last_step_app_action=sch.last_step_approver.status if sch.last_step_approver else None,
                                        last_step_app_action_at=HelperService().no_timezone(sch.last_step_approver.confirm_at) if sch.last_step_approver else None,
                                        last_step_app_action_remarks=sch.last_step_approver.confirm_remarks if sch.last_step_approver else None
                                    )

        await crud.workflow_history.create(obj_in=obj_in)

        if obj_updated.entity == WorkflowEntityEnum.MEMO and obj_updated.last_status == WorkflowLastStatusEnum.COMPLETED:
            url = f'{request.base_url}arsip/memo/task'
            GCloudTaskService().create_task(payload={"id":str(obj_updated.reference_id)}, base_url=url)
    
workflow = CRUDWorkflow(Workflow)