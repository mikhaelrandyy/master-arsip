from models.base_model import BaseULIDModel
from sqlmodel import SQLModel, Field, Relationship
from models.doc_type_departement_model import DocTypeDepartement
from typing  import TYPE_CHECKING

if TYPE_CHECKING:
    from models import DocType

class DepartementBase(SQLModel):
    code: str | None = Field(nullable=True, unique=True)
    name: str | None = Field(nullable=True)

class DepartementFullBase(BaseULIDModel, DepartementBase):
    pass

class Departement(DepartementFullBase, table=True):
    doc_types: list["DocType"] = Relationship(link_model=DocTypeDepartement, sa_relationship_kwargs={"lazy": "select", "viewonly":True})
    
    @property
    def jumlah_doc_type(self) -> int | None:
        return len(self.doc_types)