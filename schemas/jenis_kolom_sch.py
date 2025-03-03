from models.type_column_model import ColumnTypeBase, ColumnTypeFullBase
from models.base_model import SQLModel


class JenisKolomCreateSch(ColumnTypeBase):
    pass

class JenisKolomSch(ColumnTypeFullBase):
    pass 

class JenisKolomUpdateSch(ColumnTypeBase):
    pass

class JenisKolomByIdSch(ColumnTypeFullBase):
    pass

class jenisKolomByIdForMappingSch(SQLModel):
    id: str | None