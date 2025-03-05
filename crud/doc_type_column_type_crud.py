from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_crud import CRUDBase
from models import DocTypeColumn
from schemas.doc_type_sch import DocTypeSch
from schemas.doc_type_column_sch import DocTypeColumnSch, DocTypeColumnCreateSch, DocTypeColumnUpdateSch, DocTypeColumnCreateUpdateSch
import crud


class CRUDMappingDocTypeJenisKolomLink(CRUDBase[DocTypeColumnSch, DocTypeColumnCreateSch, DocTypeColumnUpdateSch]):
    async def get_by_doc_type_id(self, *, doc_type_id:str) -> list[DocTypeColumn]:

        query = select(DocTypeColumn)
        query = query.where(DocTypeColumn.doc_type_id == doc_type_id)
        response = await db.session.execute(query)
        return response.scalars().all()

    async def get_by_doc_type_column_type(self, *, doc_type_id: str, column_type_id:str) -> DocTypeColumn:

        query = select(DocTypeColumn)
        query = query.where(and_(DocTypeColumn.doc_type_id == doc_type_id,
                                 DocTypeColumn.column_type_id == column_type_id))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def mapping_doc_type_column_type(self, *, sch: DocTypeColumnCreateUpdateSch, db_session: AsyncSession | None = None):
        db_session = db_session or db.session

        for obj_in in sch.column_types:
            mapping_db = await crud.doc_type_column_type.get_by_doc_type_id(doc_type_id=sch.doc_type_id)

            if mapping_db:
                #UPDATE
                doc_type_column = await crud.doc_type_column_type.get_by_doc_type_column_type(doc_type_id=sch.doc_type_id, column_type_id=obj_in)

                if doc_type_column is None:

                    column_type = await crud.column_type.get(id=obj_in)

                    if not column_type:
                        raise HTTPException(status_code=404, detail=f"Jenis Kolom tidak tersedia")

                    create_column = DocTypeColumn(doc_type_id=sch.doc_type_id, column_type_id=obj_in)
                    db_session.add(create_column)
                    
                else:
                    mapping_db.remove(doc_type_column)

                for remove in mapping_db:
                    await crud.doc_type_column_type.remove(doc_type_id=remove.doc_type_id, column_type_id=remove.column_type_id)

            else:
                #CREATE
                add_mapping = DocTypeColumn(doc_type_id=sch.doc_type_id, column_type_id=obj_in)
                db_session.add(add_mapping) 

        await db_session.commit()

        return sch.doc_type_id

    async def remove(self, *, doc_type_id:str, column_type_id: str, db_session: AsyncSession | None = None) -> DocTypeColumn:
        db_session = db_session or db.session

        query = select(DocTypeColumn)
        query = query.where(and_(DocTypeColumn.doc_type_id == doc_type_id,
                                 DocTypeColumn.column_type_id == column_type_id))

        response = await db_session.execute(query)
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj


doc_type_column_type = CRUDMappingDocTypeJenisKolomLink(DocTypeColumn)
