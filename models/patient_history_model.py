from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class PatientHistory(Base):
    __tablename__ = 'patient_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    consultation_reason = Column(String, nullable=False)
    allergic = Column(String, nullable=False)
    medical_history = Column(String, nullable=False)
    pharmacological_history = Column(String, nullable=False)
    surgical_history = Column(String, nullable=False)
    suggested_service_type = Column(String, nullable=False)
    medical_recommendations  = Column(String, nullable=False)
    pharmacological_recommendations = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
