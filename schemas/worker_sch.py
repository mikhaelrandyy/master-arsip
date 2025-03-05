from models.worker_model import WorkerBase, WorkerFullBase
from schemas.role_sch import RoleCreateForMappingSch
from schemas.project_sch import ProjectCreateForMappingSch

class WorkerCreateSch(WorkerBase):
    departement_id: str | None
    roles: list[RoleCreateForMappingSch] | None
    projects: list[ProjectCreateForMappingSch] | None
 
class WorkerSch(WorkerFullBase):
    roles: list[RoleCreateForMappingSch] | None
    projects: list[ProjectCreateForMappingSch] | None

class WorkerUpdateSch(WorkerBase):
    pass

class WorkerByIdSch(WorkerFullBase):
    pass
