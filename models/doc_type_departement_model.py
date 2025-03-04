from models.base_model import BaseULIDModel, SQLModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Departement

class DocTypeDepartementBase(SQLModel):
    doc_type_id: str = Field(nullable=False, foreign_key='doc_type.id', primary_key=True)
    departement_id: str = Field(nullable=False, foreign_key='departement.id', primary_key=True)
    
class DocTypeDepartement(DocTypeDepartementBase, table=True):
    departement: "Departement" = Relationship(sa_relationship_kwargs = {"lazy": "select"})