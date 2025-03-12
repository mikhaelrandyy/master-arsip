from models.company_model import Company, CompanyBase
from sqlmodel import SQLModel

class CompanyCreateSch(CompanyBase):
    pass

class CompanySch(CompanyBase):
    pass

class CompanyUpdateSch(CompanyBase):
    pass

class CompanyByIdSch(CompanyBase):
    pass
