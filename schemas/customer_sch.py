from models.customer_model import CustomerBase, CustomerFullBase
from sqlmodel import SQLModel

class CustomerCreateSch(CustomerBase):
    pass

class CustomerSch(CustomerFullBase):
    pass

class CustomerUpdateSch(CustomerBase):
    pass

class CustomerByIdSch(CustomerFullBase):
    pass
