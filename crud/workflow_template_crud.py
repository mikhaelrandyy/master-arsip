from fastapi_async_sqlalchemy import db
from sqlmodel import select

from common.enum import WorkflowEntityEnum
from crud.base_crud import CRUDBase
from models.workflow_model import WorkflowTemplate
from schemas.workflow_template_sch import WorkflowTemplateCreateSch, WorkflowTemplateUpdateSch


class CRUDWorkflowTemplate(CRUDBase[WorkflowTemplate, WorkflowTemplateCreateSch, WorkflowTemplateUpdateSch]):
    async def get_by_entity(self, *, entity: WorkflowEntityEnum | None = None) -> WorkflowTemplate | None:
        response = await db.session.execute(select(self.model).where(self.model.entity == entity))
        return response.scalar_one_or_none()
    
    async def get_by_flow_id(self, *, flow_id: str | None = None) -> WorkflowTemplate | None:
        response = await db.session.execute(select(self.model).where(self.model.flow_id == flow_id))
        return response.scalar_one_or_none()

workflow_template = CRUDWorkflowTemplate(WorkflowTemplate)