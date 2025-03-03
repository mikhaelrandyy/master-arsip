from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from crud.base_crud import CRUDBase
from models import ColumnType
from schemas.jenis_kolom_sch import JenisKolomCreateSch, JenisKolomUpdateSch


class CRUDJenisKolom(CRUDBase[ColumnType, JenisKolomCreateSch, JenisKolomUpdateSch]):
    async def get_by_id(self, *, id:str) -> ColumnType:

        query = select(ColumnType)
        query = query.where(ColumnType.id == id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
     
jenis_kolom = CRUDJenisKolom(ColumnType)
