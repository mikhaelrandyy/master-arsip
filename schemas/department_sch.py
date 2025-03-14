from models.department_model import DepartmentBase, DepartmentFullBase
from schemas.doc_type_sch import DocTypeSch
from sqlmodel import SQLModel


class DepartmentCreateSch(DepartmentBase):
    pass

class DepartmentSch(DepartmentFullBase):
    number_of_doc_types: int | None = None


class DepartmentUpdateSch(DepartmentBase):
    pass

class DepartmentByIdSch(DepartmentSch):
     doc_types: list[DocTypeSch] | None = None


