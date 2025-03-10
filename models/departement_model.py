from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from models.departement_doc_type_model import DepartementDocType
from typing  import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocType, Worker

class DepartementBase(SQLModel):
    code: str | None = Field(nullable=False, default=None, unique=True)
    name: str | None = Field(nullable=True)

class DepartementFullBase(BaseULIDModel, DepartementBase):
    pass

class Departement(DepartementFullBase, table=True):
    doc_types: list["DocType"] = Relationship(link_model=DepartementDocType, sa_relationship_kwargs={"lazy": "select"})
    
    @property
    def jumlah_doc_type(self) -> int | None:
        return len(self.doc_types)