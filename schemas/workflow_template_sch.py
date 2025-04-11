from models.workflow_model import WorkflowTemplate, WorkflowTemplateBase, WorkflowTemplateFullBase
from sqlmodel import SQLModel, Field
from datetime import date, datetime

class WorkflowTemplateCreateSch(WorkflowTemplateBase):
    pass

class WorkflowTemplateSch(WorkflowTemplateFullBase):
    pass


class WorkflowTemplateUpdateSch(WorkflowTemplateBase):
    pass