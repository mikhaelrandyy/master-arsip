from sqlmodel import SQLModel, Field
from models.base_model import BaseULIDModel
 
class CompanyBase(SQLModel):
    code: str = Field(nullable=False, max_length=10, unique=True)
    name: str = Field(nullable=False, max_length=255)

class Company(CompanyBase, BaseULIDModel, table=True):
    pass