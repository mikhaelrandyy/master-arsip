from models.land_bank_model import LandBank, LandBankBase

class LandBankCreateSch(LandBankBase):
    pass

class LandBankSch(LandBank):
    project_code: str
    company_code: str

class LandBankUpdateSch(LandBankBase):
    pass

class LandBankByIdSch(LandBankBase):
    project_code: str
    company_code: str
