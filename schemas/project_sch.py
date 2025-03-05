from models.project_model import ProjectBase, ProjectFullBase
from sqlmodel import SQLModel

class ProjectCreateSch(ProjectBase):
    pass

class ProjectSch(ProjectFullBase):
    pass

class ProjectUpdateSch(ProjectBase):
    pass

class ProjectByIdSch(ProjectFullBase):
    pass

class ProjectCreateForMappingSch(SQLModel):
    id: str | None
    name: str | None