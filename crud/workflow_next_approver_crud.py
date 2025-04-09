from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import exc
from crud.base_crud import CRUDBase
from models.workflow_model import WorkflowNextApprover
from schemas.workflow_next_approver_sch import WorkflowNextApproverCreateSch, WorkflowNextApproverUpdateSch
from uuid import UUID

class CRUDWorkflowNextApprover(CRUDBase[WorkflowNextApprover, WorkflowNextApproverCreateSch, WorkflowNextApproverUpdateSch]):
    async def delete_by_workflow_id(self, *, workflow_id:UUID, with_commit:bool | None = True) -> bool:
        query = self.model.__table__.delete().where(self.model.workflow_id == workflow_id)

        try:
            await db.session.execute(query)
            if with_commit:
                await db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            raise HTTPException(status_code=422, detail="failed delete data")

        return True

workflow_next_approver = CRUDWorkflowNextApprover(WorkflowNextApprover)