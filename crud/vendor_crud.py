from crud.base_crud import CRUDBase
from models.vendor_model import Vendor
from schemas.vendor_sch import VendorCreateSch, VendorUpdateSch


class CRUDVendor(CRUDBase[Vendor, VendorCreateSch, VendorUpdateSch]):
    pass

vendor = CRUDVendor(Vendor)
