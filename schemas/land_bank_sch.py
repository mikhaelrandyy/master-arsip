from models.land_bank_model import LandBank, LandBankBase
from decimal import Decimal

class LandBankCreateSch(LandBankBase):
    pass

class LandBankSch(LandBank):
    project_code: str
    company_code: str
    luas_pemisah: Decimal | None = 0
    sisa_luas: Decimal | None = 0

class LandBankUpdateSch(LandBankBase):
    pass

class LandBankByIdSch(LandBankBase):
    project_code: str
    company_code: str
