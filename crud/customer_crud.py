from crud.base_crud import CRUDBase
from models.customer_model import customer
from schemas.customer_sch import CustomerCreateSch, CustomerUpdateSch


class CRUDCustomer(CRUDBase[customer, CustomerCreateSch, CustomerUpdateSch]):
    pass

customer = CRUDCustomer(customer)
