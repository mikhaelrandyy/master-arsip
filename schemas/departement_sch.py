from models.departement_model import DepartementBase, DepartementFullBase
from sqlmodel import SQLModel
from schemas.doc_type_sch import DocTypeCreateForDepartementSch


class DepartementCreateSch(DepartementBase):
    pass

class DepartementSch(DepartementFullBase):
    jumlah_doc_type: int | None

class DepartementUpdateSch(DepartementBase):
    pass

class DepartementByIdSch(DepartementFullBase):
    doc_types: list[DocTypeCreateForDepartementSch] | None

class DepartementCreateForMappingSch(SQLModel):
    id: str | None
    doc_types: list[DocTypeCreateForDepartementSch] | None


