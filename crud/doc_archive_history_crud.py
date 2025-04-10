from fastapi_async_sqlalchemy import db
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from crud.base_crud import CRUDBase
from models import DocArchiveHistory, Memo, DocArchive, Workflow
from sqlmodel import select, cast, String, or_, func, case
from schemas.doc_archive_history_sch import DocArchiveHistoryCreateSch, DocArchiveHistoryUpdateSch
from schemas.oauth import AccessToken
from common.enum import WorkflowLastStatusEnum


class CRUDDocArchiveHistory(CRUDBase[DocArchiveHistory, DocArchiveHistoryCreateSch, DocArchiveHistoryUpdateSch]):    
    async def fetch_history_by_doc_archive(self, doc_archive_id:str):
            query = self.base_query()
            query = query.where(DocArchiveHistory.doc_archive_id == doc_archive_id)

            response = await db.session.execute(query)
            return response.one_or_none()
    
    # async def get_paginated(self, *, params: Params | None = Params(), login_user: AccessToken | None = None, **kwargs):
    #     query = self.base_query()
    #     query = self.create_filter(login_user=login_user, query=query, filter=kwargs)

    #     return await paginate(db.session, query, params)
    
    # async def get_no_paginated(self, **kwargs):
    #     query = self.base_query()
    #     query = self.create_filter(query=query, filter=kwargs)
    #     response = await db.session.execute(query)

    #     return response.mappings().all()
    
    def base_query(self):

        query = select(
                *DocArchiveHistory.__table__.columns,
                Memo.code.label('memo_code'),
                Memo.doc_category.label('doc_category'),
                Memo.outgoing_doc_type.label('outgoing_doc_type'),
                Memo.necessity.label('necessity'),
                Memo.return_date.label('return_date'),
                DocArchive.safe_location.label('safe_location'),
                case((Workflow.last_status.in_([WorkflowLastStatusEnum.COMPLETED]), Workflow.last_status_at),
                else_= None).label('last_status_at'),
                Memo.remarks.label('description'),
            )
        

        query = query.outerjoin(Memo, Memo.id == DocArchiveHistory.memo_id
                    ).outerjoin(DocArchive, DocArchive.id ==  DocArchiveHistory.doc_archive_id
                    ).outerjoin(Workflow, Workflow.id == Memo.workflow_id)

        # workflow_subq = (
        #     select(
        #         Workflow.id.label('workflow_id)
        #         Workflow.last_status_at.label('last_status_at')
        #     ).join(Memo, Memo.workflow_id == Workflow.id)
        #     .where(Workflow.last_status == WorkflowLastStatusEnum.COMPLETED)
        # ).subquery()
        
        # query = select(
        #     *DocArchiveHistory.__table__.columns,
        #     Memo.code.label('memo_code'),
        #     Memo.doc_category.label('doc_category'),
        #     Memo.outgoing_doc_type.label('outgoing_doc_type'),
        #     Memo.necessity.label('necessity'),
        #     Memo.return_date.label('return_date'),
        #     DocArchive.safe_location.label('safe_location'),
        #     workflow_subq.c.last_status_at.label('last_status_at'),
        #     Memo.remarks.label('description'),
        # )

        # query = query.outerjoin(Memo, Memo.id == DocArchiveHistory.memo_id
        #            ).outerjoin(DocArchive, DocArchive.id ==  DocArchiveHistory.doc_archive_id
        #            ).outerjoin(workflow_subq, workflow_subq.c.id == Memo.workflow_id)
        
        return query

doc_archive_history = CRUDDocArchiveHistory(DocArchiveHistory)