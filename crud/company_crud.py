from crud.base_crud import CRUDBase
from models.company_model import Company
from schemas.company_sch import CompanyCreateSch, CompanyUpdateSch


class CRUDCompany(CRUDBase[Company, CompanyCreateSch, CompanyUpdateSch]):
    pass

company = CRUDCompany(Company)
