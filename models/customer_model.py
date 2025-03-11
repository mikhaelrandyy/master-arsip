from sqlmodel import Field
from models.base_model import BaseULIDModel, SQLModel


class CustomerBase(SQLModel):
    code: str | None = Field(nullable=True, max_length=50)
    type: str = Field(nullable=False, max_length=100)
    first_name: str | None = Field(nullable=True, max_length=40)
    last_name: str | None = Field(nullable=True, max_length=40)
    known_as: str | None = Field(nullable=True, max_length=40)
    holding: str | None = Field(nullable=True, max_length=200)
    business_id_type: str = Field(nullable=False, max_length=50)
    business_id: str = Field(nullable=False, max_length=50)
    npwp: str | None = Field(nullable=True, max_length=50)
    religion: str | None = Field(nullable=True, max_length=50)
    gender: str | None = Field(nullable=True, max_length=50)
    marital_status: str | None = Field(nullable=True, max_length=50)
    address: str = Field(nullable=False, max_length=200)
    city: str = Field(nullable=False, max_length=200)
    region: str = Field(nullable=False, max_length=200)
    country: str = Field(nullable=False, max_length=50)
    postal_code: str = Field(nullable=False, max_length=10)
    email: str = Field(nullable=False, max_length=200)
    handphone_num: str = Field(nullable=False, max_length=50)
    telp_num: str | None = Field(nullable=True, max_length=50)
    

class CustomerFullBase(CustomerBase, BaseULIDModel):
    pass


class Customer(CustomerFullBase, table=True):
   pass