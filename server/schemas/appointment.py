from pydantic import BaseModel
from datetime import date, time

from consts import AppointmentStatus

class AppointmentRequest(BaseModel):
    doctor_id: int
    booking_date: date
    booking_time: time

class AppointmentBase(BaseModel):
    id: str
    patient_id: int
    doctor_id: int
    scheduled_at: date
    status: AppointmentStatus

class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus
