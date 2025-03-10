from models.departement_doc_type_model import DepartementDocTypeBase

class DepartementDocTypeCreateSch(DepartementDocTypeBase):
    pass

class DepartementDocTypeSch(DepartementDocTypeBase):
    doc_type_name: str | None = None

class DepartementDocTypeUpdateSch(DepartementDocTypeBase):
    pass

class DepartementDocTypeByIdSch(DepartementDocTypeBase):
    pass