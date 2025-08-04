from database import Base
from sqlalchemy import Column, String, Integer, JSON

class Doctors(Base):
    __tablename__ = "doctorslist"
    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String, nullable=False)
    doctor_speciality = Column(String, nullable=False)
    doctor_experience = Column(Integer, nullable=False)
    avalibility = Column(String, nullable=False)

class UserAppointment(Base):
    __tablename__ = "userappointment"
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    useremail = Column(String, nullable=False)
    userphone = Column(String, nullable=False)
    currentTime = Column(String, nullable=False)
    time = Column(String , nullable=False)
    doctor = Column(JSON, nullable=False)