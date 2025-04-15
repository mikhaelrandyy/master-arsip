from models.land_bank_model import LandBank, LandBankBase, LandBankFullBase
from decimal import Decimal
from typing import Optional

class LandBankCreateSch(LandBankBase):
    pass

class LandBankSch(LandBankFullBase):
    company_code: str
    company_name: str
    desa_code: str
    desa_name: str
    project_code: str
    project_name: str
    alashak_name: str | None
    parent_code: str | None
    luas_pemisah: float | None
    sisa_luas: float | None

class LandBankUpdateSch(LandBankBase):
    pass

class LandBankByIdSch(LandBankSch):
    pass

# class LandBankByIdSch(LandBankFullBase):
#     company_name: str
#     company_code: str
#     project_name: str
#     project_code: str
#     desa_name: str
#     alashak_name: str
#     parent_code: str