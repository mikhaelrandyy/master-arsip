from crud.base_crud import CRUDBase
from models.workflow_model import WorkflowHistory
from schemas.workflow_history_sch import WorkflowHistoryCreateSch, WorkflowHistoryUpdateSch

class CRUDWorkflowHistory(CRUDBase[WorkflowHistory, WorkflowHistoryCreateSch, WorkflowHistoryUpdateSch]):
    pass

workflow_history = CRUDWorkflowHistory(WorkflowHistory)