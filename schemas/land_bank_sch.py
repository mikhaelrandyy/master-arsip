from models.land_bank_model import LandBank, LandBankBase
from decimal import Decimal
from typing import Optional

class LandBankCreateSch(LandBankBase):
    pass

class LandBankSch(LandBank):
    project_code: str
    company_code: str
    luas_pemisah: float | None
    sisa_luas: float | None

class LandBankUpdateSch(LandBankBase):
    pass

class LandBankByIdSch(LandBankBase):
    project_code: str
    company_code: str
