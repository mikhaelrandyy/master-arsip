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
    ARSIP_AJB = "ARSIP AJB"
    ARSIP_HOLDING = "ARSIP HOLDING"
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

class DataTypeEnum(str, Enum):
    ENUM = "ENUM"
    DATE_PICKER = "DATE PICKER"
    DATE_TIME_PICKER = "DATE TIMEPICKER"
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"

class CodeCounterEnum(str, Enum):
    DOC_FORMAT = "CDF"
    DOC_TYPE = "CJD"
    DOC_TYPE_GROUP = "GJD"

class CustomerDevEnum(str, Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    PERSON_GROUP = "person group"

class JenisIdentitasEnum(str, Enum):
    KTP = "ktp"
    NIB = "nib"
    KIA = "kia"
    PASPOR = "paspor"

class ReligionEnum(str, Enum):
    ISLAM = "islam"
    KRISTEN = "kristen"
    KATHOLIK ="katholik"
    HINDU = "hindu"
    BUDDHA = "buddha"
    KONGHUCU = "khonghucu"
    UNKNOWN = "-"

class GenderEnum(str, Enum):
    MALE = "laki - laki"
    FEMALE = "perempuan"

class MaritalStatusEnum(str, Enum):
    BELUM_KAWIN = "belum kawin"
    KAWIN = "kawin"
    CERAI_HIDUP = "cerai hidup"
    CERAI_MATI = "cerai mati"
    UNKNOWN = "-"

class AddressEnum(str, Enum):
    HOME = "rumah"
    OFFICE = "kantor"
    COMPANY = "perusahaan"
    WAREHOUSE = "gudang"
    OTHER = "lainnya"
    UNKNOWN = "-"






