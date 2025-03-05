from crud.base_crud import CRUDBase
from models.project_model import Project
from schemas.project_sch import ProjectCreateSch, ProjectUpdateSch


class CRUDProject(CRUDBase[Project, ProjectCreateSch, ProjectUpdateSch]):
    pass

project = CRUDProject(Project)
