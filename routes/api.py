from fastapi import APIRouter, Depends
from configs.permission import Permission
from routes.endpoints import department, doc_format, doc_type, doc_type_group, column_type, alashak, worker, role, project

api_router = APIRouter(dependencies=[Depends(Permission().get_login_user)])

# api_router = APIRouter()

api_router.include_router(doc_format.router, prefix="/doc-format", tags=["doc_format"])
api_router.include_router(doc_type.router, prefix="/doc-type", tags=["doc_type"])
api_router.include_router(doc_type_group.router, prefix="/doc-type-group", tags=["doc_type_group"])
api_router.include_router(column_type.router, prefix="/column-type", tags=["column_type"])
api_router.include_router(alashak.router, prefix="/alashak", tags=["alashak"])
api_router.include_router(department.router, prefix="/department", tags=["department"])
api_router.include_router(worker.router, prefix="/worker", tags=["worker"])
api_router.include_router(role.router, prefix="/role", tags=["role"])
api_router.include_router(project.router, prefix="/project", tags=["project"])








