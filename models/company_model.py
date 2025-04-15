from sqlmodel import Field
from models.base_model import BaseULIDModel, SQLModel
 
class CompanyBase(SQLModel):
    code: str = Field(nullable=False, max_length=10, unique=True)
    name: str = Field(nullable=False, max_length=255)

class CompanyFullBase(CompanyBase, BaseULIDModel):
    pass

class Company(CompanyFullBase, table=True):
    pass