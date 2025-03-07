from fastapi_async_sqlalchemy import db
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from crud.base_crud import CRUDBase
from models import Worker, WorkerRole
from schemas.worker_sch import WorkerCreateSch, WorkerUpdateSch
from itertools import product
import crud

class CRUDWorker(CRUDBase[Worker, WorkerCreateSch, WorkerUpdateSch]):
    async def get_by_id(self, *, id:str) -> Worker:

        query = select(Worker)
        query = query.where(Worker.id == id)
        query = query.options(selectinload(Worker.roles), selectinload(Worker.departement))
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def get_by_client_id(self, *, client_id:str) -> Worker:

        query = select(Worker)
        query = query.where(Worker.client_id == client_id)
        response = await db.session.execute(query)
        return response.scalar_one_or_none()
    
    async def create(self, *, sch:WorkerCreateSch, created_by:str, db_session: AsyncSession | None = None) -> Worker:
        db_session = db_session or db.session

        worker = Worker.model_validate(sch.model_dump())
        db_session.add(worker)

        await db_session.flush()

        for role in sch.roles:
            mapping = WorkerRole(worker_id=worker.id, role_id=role.id)
            db_session.add(mapping)

        if created_by:
            worker.created_by = worker.updated_by = created_by

        await db_session.commit()

        return worker
        
worker = CRUDWorker(Worker)
