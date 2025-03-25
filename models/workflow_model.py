from sqlmodel import SQLModel, Field, Relationship
from common.enum import WorkflowLastStatusEnum, WorkflowEntityEnum
from models.base_model import BaseULIDModel
from datetime import datetime
from pydantic import EmailStr

class WorkflowBase(SQLModel):
    reference_id: str = Field(nullable=False) 
    txn_id: str | None = Field(nullable=True) #id object workflow
    step_name: str | None = Field(nullable=True)
    last_status: WorkflowLastStatusEnum | None = Field(nullable=True)
    last_status_at: datetime | None = Field(nullable=True)
    last_step_app_email: str | None = Field(nullable=True)
    last_step_app_name: str | None = Field(nullable=True)
    last_step_app_action: str | None = Field(nullable=True)
    last_step_app_action_at: datetime | None = Field(nullable=True)
    last_step_app_action_remarks: str | None = Field(nullable=True)
    entity: WorkflowEntityEnum | None = Field(nullable=False)
    flow_id: str | None = Field(nullable=False)
    version: int | None = Field(default=1)

class WorkflowFullBase(BaseULIDModel, WorkflowBase):
    pass

class Workflow(WorkflowFullBase, table=True):
    pass


class WorkflowNextApproverBase(SQLModel):
    workflow_id: str = Field(nullable=False, foreign_key="workflow.id")
    email: EmailStr | None = Field(nullable=True)
    name: str | None = Field(nullable=True)

class WorkflowNextApproverFullBase(BaseULIDModel, WorkflowNextApproverBase):
    pass

class WorkflowNextApprover(WorkflowNextApproverFullBase, table=True):
    pass


class WorkflowHistoryBase(SQLModel):
    workflow_id: str | None = Field(foreign_key="workflow.id", nullable=False)
    step_name: str | None = Field(nullable=True)
    last_status: WorkflowLastStatusEnum | None = Field(nullable=True)
    last_status_at: datetime | None = Field(nullable=True)
    last_step_app_email: str | None = Field(nullable=True)
    last_step_app_name: str | None = Field(nullable=True)
    last_step_app_action: str | None = Field(nullable=True)
    last_step_app_action_at: datetime | None = Field(nullable=True)
    last_step_app_action_remarks: str | None = Field(nullable=True)

class WorkflowHistoryFullBase(BaseULIDModel, WorkflowHistoryBase):
    pass

class WorkflowHistory(WorkflowHistoryFullBase, table=True):
    pass


class WorkflowTemplateBase(SQLModel):
    entity: WorkflowEntityEnum | None
    flow_id: str | None

class WorkflowTemplateFullBase(WorkflowTemplateBase, BaseULIDModel):
    pass

class WorkflowTemplate(WorkflowTemplateFullBase, table=True):
    pass