from sqlmodel import SQLModel, Field
from models.base_model import BaseFieldULIDModel
from common.enum import CodeCounterEnum

class CodeCounterBase(SQLModel):
    entity: CodeCounterEnum | None
    last: int | None = Field(default=1, nullable=True)
    digit: int | None = Field(default=5, nullable=True)

class CodeCounter(BaseFieldULIDModel, CodeCounterBase, table=True):
    pass
