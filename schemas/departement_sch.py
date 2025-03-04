from models.departement_model import DepartementBase, DepartementFullBase
from models.base_model import SQLModel
from schemas.doc_type_sch import DocTypeCreateForDepartementSch


class DepartementCreateSch(DepartementBase):
    pass

class DepartementSch(DepartementFullBase):
    jumlah_doc_type: int | None
    doc_types: list[DocTypeCreateForDepartementSch] | None

class DepartementUpdateSch(DepartementBase):
    pass

class DepartementByIdSch(DepartementFullBase):
    pass

class DepartementCreateForMappingSch(DepartementBase):
    doc_types: list[DocTypeCreateForDepartementSch] | None


