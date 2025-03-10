from models.column_type_model import ColumnTypeBase, ColumnTypeFullBase
from models.base_model import SQLModel


class ColumnTypeCreateSch(ColumnTypeBase):
    pass

class ColumnTypeSch(ColumnTypeFullBase):
    pass 

class ColumnTypeUpdateSch(ColumnTypeBase):
    pass

class ColumnTypeByIdSch(ColumnTypeFullBase):
    pass

class ColumnTypeByIdForMappingSch(SQLModel):
    id: str | None