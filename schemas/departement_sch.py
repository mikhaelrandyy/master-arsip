from models.departement_model import DepartementBase, DepartementFullBase
from sqlmodel import SQLModel


class DepartementCreateSch(DepartementBase):
    pass

class DepartementSch(DepartementFullBase):
    jumlah_doc_type: int | None

class DepartementUpdateSch(DepartementBase):
    pass

class DepartementByIdSch(DepartementFullBase):
    pass

class DepartementCreateForMappingSch(SQLModel):
    id: str | None


