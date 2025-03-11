from models.company_model import CompanyBase, CompanyFullBase
from sqlmodel import SQLModel

class CompanyCreateSch(CompanyBase):
    pass

class CompanySch(CompanyFullBase):
    pass

class CompanyUpdateSch(CompanyBase):
    pass

class CompanyByIdSch(CompanyFullBase):
    pass
