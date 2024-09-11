from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from config.database import Session
from models.physician_model import Physician as PhysicianModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

physician_router = APIRouter()
templates = Jinja2Templates(directory="templates")


class Physician(BaseModel):
    name: str
    last_name: str
    identity_card: str
    residence_place: str
    residence_address: str
    phone_number: str
    email: str
    bank: str
    bank_account_number: str
    class Config:
        from_attributes = True

# physician = [{}]


# INFO: Physician Creation
# @physician_router.get('/physician', tags=['Physician'])
# async def get_physician():
#     db = Session()
#     result = db.query(PhysicianModel).all()
#     return JSONResponse(content=jsonable_encoder(result))

@physician_router.get('/physician', response_class=HTMLResponse, tags=['Physician'])
async def get_physician_form(request: Request):
    return templates.TemplateResponse("creation_physician.html", {"request": request})




@physician_router.get(f'/physician/{id}', tags=['Physician'])
async def get_physician_by_id(id: int):
    db = Session()
    physician = db.query(PhysicianModel).filter(PhysicianModel.id == id)
    return [Physician.from_orm(i) for i in physician]
    return JSONResponse(content=jsonable_encoder(result))

@physician_router.post('/physician/', tags=['Physician'])
async def create_physician(physician: Physician) -> JSONResponse:
    db = Session()
    new_physician = PhysicianModel(**physician.model_dump())
    db.add(new_physician)
    db.commit()
    return JSONResponse(content={'Se ha creado el Médico'})

@physician_router.get('/physician_name', tags=['Physician'])
async def get_physician_name():
    db = Session()
    result = db.query(PhysicianModel).all()
    physi = [{"id": i.id, "name": i.name} for i in result]
    return JSONResponse(content=jsonable_encoder(physi))
