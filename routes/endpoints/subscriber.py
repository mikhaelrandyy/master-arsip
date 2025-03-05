from fastapi import Request, APIRouter, Query
from crud.project_crud import project
from schemas.response_sch import PostResponseBaseSch, create_response
from services.pubsub_service import PubSubService
from models.project_model import Project

router = APIRouter()
pub_sub_service = PubSubService()

@router.post("/master_project", response_model=PostResponseBaseSch[bool])
async def subscribe_create_project(request: Request, base64Str: str|None = Query(description="Base64 from object", default=None)):
    message_object = await pub_sub_service.generatePublisherMessage(request, base64Str)
    newProject:Project = Project(**message_object)
    obj = await project.get(id=newProject.id)
    if obj:
        await project.update(obj_current=obj, obj_new=newProject)
    else:
        await project.create(obj_in=newProject)        
    return create_response(data=True) 