from fastapi import APIRouter, Depends
from configs.permission import Permission
from routes.endpoints import department, doc_format, doc_type, doc_type_group, column_type, alashak, worker, role, project, desa, memo, company, workflow, land_bank

api_router = APIRouter(dependencies=[Depends(Permission().get_login_user)])

# api_router = APIRouter()
api_router.include_router(alashak.router, prefix="/alashak", tags=["ALASHAK"])
api_router.include_router(column_type.router, prefix="/column-type", tags=["COLUMN TYPE"])
api_router.include_router(company.router, prefix="/company", tags=["COMPANY"])
api_router.include_router(department.router, prefix="/department", tags=["DEPARTMENT"])
api_router.include_router(doc_format.router, prefix="/doc-format", tags=["DOC FORMAT"])
api_router.include_router(doc_type.router, prefix="/doc-type", tags=["DOC TYPE"])
api_router.include_router(doc_type_group.router, prefix="/doc-type-group", tags=["DOC TYPE GROUP"])
api_router.include_router(memo.router, prefix="/memo", tags=["MEMO"])
api_router.include_router(land_bank.router, prefix="/land-bank", tags=["LAND BANK"])
api_router.include_router(project.router, prefix="/project", tags=["PROJECT"])
api_router.include_router(desa.router, prefix="/desa", tags=["DESA"])
api_router.include_router(role.router, prefix="/role", tags=["ROLE"])
api_router.include_router(worker.router, prefix="/worker", tags=["WORKER"])


api_router_no_auth = APIRouter()
api_router_no_auth.include_router(workflow.router, prefix="/workflow", tags=["WORKFLOW"])















