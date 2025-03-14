from models.worker_model import WorkerBase, WorkerFullBase
from schemas.role_sch import RoleCreateForMappingSch
from schemas.project_sch import ProjectCreateForMappingSch

class WorkerCreateSch(WorkerBase):
    department_id: str | None
    roles: list[RoleCreateForMappingSch] | None
 
class WorkerSch(WorkerFullBase):
    department_name: str | None

class WorkerUpdateSch(WorkerBase):
    pass

class WorkerByIdSch(WorkerFullBase):
    roles: list[RoleCreateForMappingSch] | None
