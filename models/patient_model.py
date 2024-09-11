from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    case_number = Column(Integer, nullable=False)
    date_attendance = Column(String, nullable=False)
    name = Column(String, nullable=False)
    # last_name = Column(String, nullable=False)
    data_birth = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    physician_id = Column(Integer, ForeignKey('physician.id'), nullable=False)

    historial = relationship("PatientHistory", backref="patient")
