from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from config.database import Session, Base, engine
from models.patient_model import Patient as PatientModel
from fastapi.middleware.cors import CORSMiddleware

from fastapi.encoders import jsonable_encoder
from jwt_manager import create_token
from fastapi.staticfiles import StaticFiles


from routers.patient import patient_router
from routers.physician import physician_router
from routers.auth import auth_router

app = FastAPI()

app.title = 'Unname'
app.include_router(patient_router)
app.include_router(physician_router)
app.include_router(auth_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:8080", # localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    # allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"],
    max_age=3600,  # tiempo de vida de la configuración CORS (en segundos)
)


Base.metadata.create_all(bind=engine)
