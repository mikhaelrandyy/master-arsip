from fastapi import APIRouter, Depends
from configs.permission import Permission
from routes.endpoints import document_type

api_router = APIRouter(dependencies=[Depends(Permission().get_login_user)])

api_router.include_router(document_type.router, prefix="/document-type", tags=["document_type"])
