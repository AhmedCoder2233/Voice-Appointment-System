from pydantic import BaseModel, EmailStr
import random
from datetime import datetime

class AddDoctors(BaseModel):
    doctor_name:str
    doctor_speciality:str
    doctor_experience:int
    avalibility:str

class UserAppoint(BaseModel):
    userid: int = random.randint(100,500) * 6
    username:str
    useremail:EmailStr
    userphone:str
    currentTime:str = datetime.now()
    time:str
    doctor:list