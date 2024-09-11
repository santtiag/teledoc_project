from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

class Physician(Base):
    __tablename__ ='physician'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    identity_card = Column(String, nullable=False)
    residence_place = Column(String, nullable=False)
    residence_address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    bank = Column(String, nullable=False)
    bank_account_number = Column(String, nullable=False)

    pacientes = relationship("Patient", backref="physician")
