from typing import Optional
from sqlmodel import Field
from models.base_model import SQLModel, BaseULIDModel


class UnitBase(SQLModel):
    code: str = Field(nullable=False, max_length=100, unique=True)
    descs: str = Field(nullable=False, max_length=255)
    land_area: float = Field(nullable=False)
    building_area: float = Field(nullable=False)
    indoor_area: float | None = Field(nullable=True)
    outdoor_area: float | None = Field(nullable=True)
    sales_status: int = Field(nullable=True)
    handover_status: int = Field(nullable=True)
    sub_group_id: str = Field(nullable=False)
    floor_id: str = Field(nullable=False)
    type_id: str = Field(nullable=False)
    classification_code: int = Field(nullable=True)
    address: Optional[str] = Field(nullable=True, max_length=255)
    project_id: str = Field(nullable=False)
    sub_project_id: str = Field(nullable=False)
    group_id: str = Field(nullable=False)

class UnitFullBase(UnitBase, BaseULIDModel):
    pass

class Unit(UnitFullBase, table=True):
    pass