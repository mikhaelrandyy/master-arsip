from fastapi import APIRouter, Depends
from configs.permission import Permission
from routes.endpoints import doc_format, doc_type, doc_type_group, departement, column_type, alashak

api_router = APIRouter(dependencies=[Depends(Permission().get_login_user)])

# api_router = APIRouter()

api_router.include_router(doc_format.router, prefix="/doc-format", tags=["doc_format"])
api_router.include_router(doc_type.router, prefix="/doc-type", tags=["doc_type"])
api_router.include_router(doc_type_group.router, prefix="/doc-type-group", tags=["doc_type_group"])
api_router.include_router(column_type.router, prefix="/column-type", tags=["column_type"])
api_router.include_router(alashak.router, prefix="/alashak", tags=["alashak"])
api_router.include_router(departement.router, prefix="/departement", tags=["departement"])





