from sqlmodel import SQLModel, Field
from models.base_model import BaseULIDModel

class VendorBase(SQLModel):
    code: str = Field(nullable=True, max_length=10, unique=True)
    name: str = Field(nullable=True, max_length=100)
    phone: str = Field(nullable=True, max_length=30)
    fax: str = Field(nullable=True, max_length=30)
    address: str = Field(nullable=True, max_length=255)
    is_active:bool|None = Field(nullable=False, default=True)

class VendorFullBase(VendorBase, BaseULIDModel):
    pass

class Vendor(VendorFullBase, table=True):
    pass