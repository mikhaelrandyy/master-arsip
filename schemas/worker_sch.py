from models.worker_model import WorkerBase, WorkerFullBase
from schemas.role_sch import RoleCreateForMappingSch
from schemas.project_sch import ProjectCreateForMappingSch

class WorkerCreateSch(WorkerBase):
    departement_id: str | None
    roles: list[RoleCreateForMappingSch] | None
 
class WorkerSch(WorkerFullBase):
    departement_name: str | None

class WorkerUpdateSch(WorkerBase):
    pass

class WorkerByIdSch(WorkerFullBase):
    roles: list[RoleCreateForMappingSch] | None
