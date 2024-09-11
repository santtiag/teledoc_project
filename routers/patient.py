from fastapi import APIRouter, Request, Depends
from typing import List
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from config.database import Session
from models.patient_model import Patient as PatientModel
from pydantic import BaseModel, Field, ValidationError
from fastapi.encoders import jsonable_encoder
from models.patient_history_model import PatientHistory as PatientHistoryModel
from fastapi.templating import Jinja2Templates
from routers.auth import JWTBearer

patient_router = APIRouter()
templates = Jinja2Templates(directory="templates")

class Patient(BaseModel):
    id: int = Field(primary_key=True)
    country: str
    case_number: int
    date_attendance: str
    name: str = Field(max_length=45)
    data_birth: str
    phone_number: str
    mail: str
    physician_id: int

    class Config:
        from_attributes = True

class PatientHistory(BaseModel):
    consultation_reason: str
    allergic: str
    medical_history: str
    pharmacological_history: str
    surgical_history: str
    suggested_service_type: str
    medical_recommendations: str
    pharmacological_recommendations: str
    patient_id: int


@patient_router.get('/patient', tags=['Patients'], response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def get_patients(request: Request):
    db = Session()
    physician = request.state.physician
    patients = db.query(PatientModel).filter(PatientModel.physician_id == physician.id).all()

    # Renderizar la página de pacientes con los datos
    return templates.TemplateResponse("patients_of_physician.html", {"request": request, "patients": patients, "physician_name": physician.name})


# @patient_router.get('/patient', tags=['Patients'],  response_model=List[Patient], dependencies=[Depends(JWTBearer())])
# async def get_patients(request: Request):
#     db = Session()
#     physician = request.state.physician
#     patients = db.query(PatientModel).filter(PatientModel.physician_id == physician.id).all()
#     return [Patient.from_orm(patient) for patient in patients]


# @patient_router.post('/patient', tags=['Patients'])
# async def create_patient(patient: Patient) -> JSONResponse:
#     try:
#         db = Session()
#         new_patient = PatientModel(**patient.model_dump())
#         db.add(new_patient)
#         db.commit()
#         return JSONResponse(content=['Se ha registrado el paciente'])
#     except ValidationError as e:
#         return JSONResponse(content={'error': e.errors()}, status_code=422)


# INFO: Patient Registration
# @patient_router.get('/patient_registration', tags=['Patients'], dependencies=[Depends(JWTBearer())])
# async def get_patient_registration() -> JSONResponse:
#     db = Session()
#     result = db.query(PatientHistoryModel).all()
#     return JSONResponse(content=jsonable_encoder(result))
@patient_router.get(f'/patient_registration/{id}', tags=['Patients'], response_class=HTMLResponse, dependencies=[Depends(JWTBearer)])
async def get_patient_registration(request: Request, id_paciente: int):
    return templates.TemplateResponse("patient_form.html", {"request": request, "id_paciente": id_paciente})


# @patient_router.post('/patient_registration', tags=['Patients'])
# async def create_patient_registration(patient_history: PatientHistory) -> JSONResponse:
#     db = Session()
#     new_patient_history = PatientHistoryModel(**patient_history.model_dump())
#     db.add(new_patient_history)
#     db.commit()
#     return JSONResponse(content=['Registrado'])
