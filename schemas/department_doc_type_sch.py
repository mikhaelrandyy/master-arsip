from models.department_doc_type_model import DepartmentDocTypeBase

class DepartmentDocTypeCreateSch(DepartmentDocTypeBase):
    pass

class DepartmentDocTypeSch(DepartmentDocTypeBase):
    doc_type_name: str | None = None

class DepartmentDocTypeUpdateSch(DepartmentDocTypeBase):
    pass

class DepartmentDocTypeByIdSch(DepartmentDocTypeBase):
    pass