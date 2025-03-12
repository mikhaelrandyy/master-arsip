from crud.base_crud import CRUDBase
from models.customer_model import Customer
from schemas.customer_sch import CustomerCreateSch, CustomerUpdateSch


class CRUDCustomer(CRUDBase[Customer, CustomerCreateSch, CustomerUpdateSch]):
    pass

customer = CRUDCustomer(Customer)
