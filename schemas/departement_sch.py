from models.departement_model import DepartementBase, DepartementFullBase
from schemas.doc_type_sch import DocTypeSch
from sqlmodel import SQLModel


class DepartementCreateSch(DepartementBase):
    pass

class DepartementSch(DepartementFullBase):
    number_of_doc_types: int | None = None


class DepartementUpdateSch(DepartementBase):
    pass

class DepartementByIdSch(DepartementSch):
     doc_types: list[DocTypeSch] | None = None


