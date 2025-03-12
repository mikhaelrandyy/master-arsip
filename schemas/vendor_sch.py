from models.vendor_model import VendorBase, VendorFullBase
from sqlmodel import SQLModel

class VendorCreateSch(VendorBase):
    pass

class VendorSch(VendorFullBase):
    pass

class VendorUpdateSch(VendorBase):
    pass

class VendorByIdSch(VendorFullBase):
    pass
