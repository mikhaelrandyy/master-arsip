from enum import Enum

class DocumentCategoryEnum(str, Enum):
    MASUK = "MASUK"
    KELUAR = "KELUAR"
    PINJAM = "PINJAM"
    KEMBALI = "KEMBALI"
    MASUK_HOLD = "MASUK_HOLD"
    HOLD = "HOLD"
    UNHOLD = "UNHOLD"

class DocumentClassificationEnum(str, Enum):
    ARSIP = "ARSIP"
    PBB = "PBB"
    PBT = "PBT"
    SPH_PJB_PPJB = "SPH_PJB_PPJB"
    SPS = "SPS"
    TANDA_TERIMA_KONSUMEN_BANK = "TANDA_TERIMA_KONSUMEN_BANK"
    AJB_HOLDING = "AJB_HOLDING"
    BPHTB = "BPHTB"

class NecessityEnum(str, Enum):
    KELUAR_KE_KONSUMEN = "KELUAR_KE_KONSUMEN"
    KELUAR_KE_BANK = "KELUAR_KE_BANK"
    PENGGABUNGAN = "PENGGABUNGAN"
    PROSES_AJB = "PROSES_AJB" 
    CHECK_INTERNAL = "CHECK_INTERNAL"
    PEMECAHAN = "PEMECAHAN"
    PERPANJANGAN = "PERPANJANGAN"
    REVISI = "REVISI"
    PEMISAHAN = "PEMISAHAN"
    TRANSFER = "TRANSFER"

class GroupingDocumentEnum(str, Enum):
    DATA_UTAMA = "DATA_UTAMA"
    DATA_PENDUKUNG = "DATA_PENDUKUNG"

class JenisArsipEnum(str, Enum):
    ARSIP_HOLDING = "ARSIP_HOLDING"
    ARSIP_AJB = "ARSIP_AJB"

class DataTypeEnum(str, Enum):
    ENUM = "ENUM"
    DATE_PICKER = "DATE_PICKER"
    DATE_TIME_PICKER = "DATE_TIMEPICKER"
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    ALASHAK = "ALASHAK"
    UNIT = "UNIT" 
    CUSTOMER = "CUSTOMER"
    VENDOR = "VENDOR"

class CodeCounterEnum(str, Enum):
    DOC_FORMAT = "CDF"
    DOC_TYPE = "CJD"
    DOC_TYPE_GROUP = "GJD"
    MEMO = "ASG"


class PhysicalDocTypeEnum(str, Enum):
    ASLI = "ASLI"
    DUPLIKAT = "DUPLIKAT"
    COPY = "COPY"
    LEGALISIR = "LEGALISIR"
    SALINAN = "SALINAN"

class OutgoingToTypeEnum(str, Enum):
    CUSTOMER = "CUSTOMER"
    BANK = "BANK"
    NOTARIS = "NOTARIS"
    INTERNAL = "INTERNAL"
    TRANSFER = "TRANSFER"

class OutgoingToDocTypeEnum(str, Enum):
    ASLI = "ASLI"
    COPY = "COPY"

class StatusDocArchiveEnum(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    AVAILABLE_HOLD = "AVAILABLE_HOLD"

class WorkflowEntityEnum(str, Enum):
    MEMO = "MEMO"

class WorkflowLastStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    ISSUED = "ISSUED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    NEED_DATA_UPDATE = "NEED_DATA_UPDATE"
    WAITING_APPROVAL = "WAITING_APPROVAL"

class WorkflowStepEnum(str, Enum):
    ISSUED = "ISSUED"
    SUBMITTED = "SUBMITTED"
    APPROVED_1 = "APPROVED 1"
    RECEIVED = "RECEIVED"
    CHECKED = "CHECKED"
    APPROVED_2 = "APPROVED 2"
    POSTED = "POSTED"