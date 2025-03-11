from fastapi import Request, APIRouter, Query
from schemas.response_sch import PostResponseBaseSch, create_response
from services.pubsub_service import PubSubService
from typing import TYPE_CHECKING
import crud
from crud import project, vendor, unit, customer, company

if TYPE_CHECKING:
    from models import Vendor, Project, Unit, Customer, Company

router = APIRouter()
pub_sub_service = PubSubService()

@router.post("/master_vendor", response_model=PostResponseBaseSch[bool])
async def subscribe_create_vendor(request: Request, base64Str: str|None = Query(description="Base64 from object", default=None)):
    message_object = await pub_sub_service.generatePublisherMessage(request, base64Str)
    newVendor:Vendor = Vendor(**message_object)
    obj = await crud.vendor.get(id=newVendor.id)
    if obj:
        await crud.vendor.update(obj_current=obj, obj_new=newVendor)
    else:
        await crud.vendor.create(obj_in=newVendor)        
    return create_response(data=True) 

@router.post("/master_project", response_model=PostResponseBaseSch[bool])
async def subscribe_create_project(request: Request, base64Str: str|None = Query(description="Base64 from object", default=None)):
    message_object = await pub_sub_service.generatePublisherMessage(request, base64Str)
    newProject:Project = Project(**message_object)
    obj = await crud.project.get(id=newProject.id)
    if obj:
        await crud.project.update(obj_current=obj, obj_new=newProject)
    else:
        await crud.project.create(obj_in=newProject)        
    return create_response(data=True) 

@router.post("/master_unit", response_model=PostResponseBaseSch[bool])
async def subscribe_create_unit(request: Request, base64Str: str | None = Query(description="Base64 from object", default=None)):
    message_object = await pub_sub_service.generatePublisherMessage(request, base64Str)
    newUnit: Unit = Unit(**message_object)
    obj_current = await crud.unit.get(id=newUnit.id)
    if obj_current:
        await crud.unit.update(obj_current=obj_current, obj_new=newUnit)
    else:
        await unit.create(obj_in=newUnit)
    return create_response(data=True)

@router.post("/master_customer", response_model=PostResponseBaseSch[bool])
async def subscribe_create_customer(request: Request, base64Str: str|None = Query(description="Base64 from object", default=None)):
    message_object = await pub_sub_service.generatePublisherMessage(request, base64Str)
    newCust:Customer = Customer(**message_object)
    obj = await crud.customer.get(id=newCust.id)
    if obj:
        await crud.customer.update(obj_current=obj, obj_new=newCust)
    else:
        await crud.customer.create(obj_in=newCust)
    return create_response(data=True) 

@router.post("/master_company", response_model=PostResponseBaseSch[bool])
async def subscribe_create_company(request: Request, base64Str: str|None = Query(description="Base64 from object", default=None)):
    message_object = await pub_sub_service.generatePublisherMessage(request, base64Str)
    newCompany:Company = Company(**message_object)
    obj = await crud.company.get(id=newCompany.id)
    if obj:
        await crud.company.update(obj_current=obj, obj_new=newCompany)
    else:
        await crud.company.create(obj_in=newCompany)
    return create_response(data=True) 