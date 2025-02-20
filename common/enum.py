from enum import Enum

class DocumentCategoryEnum(str, Enum):
    MASUK = "MASUK"
    KELUAR = "KELUAR"
    PINJAM = "PINJAM"
    KEMBALI = "KEMBALI"
    MASUK_HOLD = "MASUK HOLD"
    HOLD = "HOLD"
    UNHOLD = "UNHOLD"

class DocumentClassificationEnum(str, Enum):
    ARSIP_AJB = "ARSIP_AJB"
    ARSIP_HOLDING = "ARSIP_HOLDING"
    PBB = "PBB"
    PBT = "PBT"
    SPH_PJB_PPJB = "SPH/PJB/PPJB"
    SPS = "SPS"
    TANDA_TERIMA_KONSUMEN_BANK = "TANDA TERIMA KONSUMEN / BANK"
    AJB_HOLDING = "AJB HOLDING"
    BPHTH = "BPHTH"

class GroupingDocumentEnum(str, Enum):
    DATA_UTAMA = "DATA UTAMA"
    DATA_PENDUKUNG = "DATA PENDUKUNG"

class JenisArsipEnum(str, Enum):
    ARSIP_HOLDING = "ARSIP HOLDING"
    ARSIP_AJB = "ARSIP AJB"

class TipeDataEnum(str, Enum):
    ENUM = "ENUM"
    DATE_PICKER = "DATE_PICKER"
    DATE_TIME_PICKER = "DATE_TIME_PICKER"
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"



