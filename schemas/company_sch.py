from models.company_model import Company, CompanyBase, CompanyFullBase
from sqlmodel import SQLModel

class CompanyCreateSch(CompanyBase):
    pass

class CompanySch(CompanyFullBase):
    pass

class CompanyUpdateSch(CompanyBase):
    pass

class CompanyByIdSch(CompanyFullBase):
    pass
