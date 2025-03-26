from models.department_model import DepartmentBase, DepartmentFullBase
from schemas.department_doc_type_sch import DepartmentDocTypeSch
from sqlmodel import SQLModel


class DepartmentCreateSch(DepartmentBase):
    doc_type_ids: list[str] | None = None

class DepartmentSch(DepartmentFullBase):
    number_of_doc_types: int | None = None


class DepartmentUpdateSch(DepartmentBase):
    doc_type_ids: list[str] | None = None

class DepartmentByIdSch(DepartmentSch):
     doc_types: list[DepartmentDocTypeSch] | None = None


