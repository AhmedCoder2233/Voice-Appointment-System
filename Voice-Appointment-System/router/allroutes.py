from fastapi import APIRouter, Depends
from model import Base
from database import LocalSession, engine
from sqlalchemy.orm import Session
from schema import AddDoctors, UserAppoint
from model import Doctors, UserAppointment

Base.metadata.create_all(bind=engine)

router = APIRouter()

def getdb():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@router.post("/doctors")
def PostDoctors(doctors:AddDoctors, db:Session = Depends(getdb)):
    data = Doctors(**doctors.model_dump())
    db.add(data)
    db.commit()
    return "Doctors Saved Succesfully"

@router.post("/userOrder")
def placeOrder(order: UserAppoint, db: Session = Depends(getdb)):
    datasave = UserAppointment(**order.model_dump())
    db.add(datasave)
    db.commit()
    db.refresh(datasave)
    return {
        "orderid": datasave.userid,
        "message": f"Okay! Your appointment is booked. ✅ Appointment ID: {datasave.userid}. Your appointment is tomorrow. Thank you and goodbye! 👋"
    }
@router.get("/doctorslist")
def getAllDoctors(db:Session = Depends(getdb)):
    return db.query(Doctors).all()

@router.delete("/appointmentcancel/{userid}")
def CancelAppoint(userid:str, db:Session = Depends(getdb)):
    data = db.query(UserAppointment).filter(UserAppointment.userid == userid).first()
    if not data:
        return {"message": "Failed to find user with this id!"}
    db.delete(data)
    db.commit()
    return {"message": "Appointment Deleted Succesfully"}