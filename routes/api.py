from fastapi import APIRouter, Depends
from configs.permission import Permission
from routes.endpoints import doc_type_jenis_kolom, document_format, document_type, document_type_group, jenis_kolom, doc_format_jenis_arsip_doc_type_link

# api_router = APIRouter(dependencies=[Depends(Permission().get_login_user)])

api_router = APIRouter()


api_router.include_router(document_format.router, prefix="/document-format", tags=["document_format"])
api_router.include_router(document_type.router, prefix="/document-type", tags=["document_type"])
api_router.include_router(document_type_group.router, prefix="/document-type-group", tags=["document_type_group"])
api_router.include_router(jenis_kolom.router, prefix="/jenis-kolom", tags=["jenis_kolom"])
api_router.include_router(doc_format_jenis_arsip_doc_type_link.router, prefix="/doc-format-jenis-arsip-doc-type-link", tags=["doc_format_jenis_arsip_doc_type_link"])
api_router.include_router(doc_type_jenis_kolom.router, prefix="/doc-type-jenis-kolom", tags=["doc_type_jenis_kolom_link"])




