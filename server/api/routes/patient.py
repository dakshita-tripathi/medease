from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.future import select

from core.database import get_db
from models.appointment import Appointment
from schemas.appointment import AppointmentRequest, AppointmentStatusUpdate
from models.user import User
from api.deps import get_current_user
from consts import AppointmentStatus

router = APIRouter(prefix="/appointments", tags=["Patient"])

@router.get("/my")
def get_appointments_per_patient(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = db.execute(select(Appointment).where(Appointment.patient_id == current_user["id"]))
    appointments = result.scalars().all()
    return appointments

@router.post("/book")
def book_appointment(
    data: AppointmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user["role"] != "patient":
        raise HTTPException(403, "Only patients can book appointments")

    result = db.execute(
        select(User).where(
            User.id == data.doctor_id,
            User.role == "doctor"
        )
    )
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(404, "Doctor not found")
    print(current_user)
    appointment = Appointment(
        id=str(datetime.now())+str(current_user["id"])+str(data.doctor_id),
        patient_id=current_user["id"],
        doctor_id=data.doctor_id,
        scheduled_at=datetime.now(),
        status= "requested",
        booking_date=data.booking_date,
        booking_time=data.booking_time
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

@router.patch("/{appointment_id}/status")
def update_appointment_status(
    appointment_id: str,
    data: AppointmentStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    print(appointment.patient_id)
    if not appointment:
        raise HTTPException(404, "Appointment not found")

    if current_user["role"] == "patient":
        if appointment.patient_id != current_user["id"]:
            print(appointment.patient_id, current_user["id"])
            print(type(appointment.patient_id), type(current_user["id"]))
            raise HTTPException(403, "Not an appointment you can edit")
        if data.status != AppointmentStatus.cancelled:
            raise HTTPException(403, "Patients can only cancel appointments")

    elif current_user["role"] == "doctor":
        if appointment.doctor_id != current_user["id"]:
            raise HTTPException(403, "Not your appointment")

    else:
        raise HTTPException(403, "Unauthorized role")

    appointment.status = data.status

    db.commit()
    db.refresh(appointment)

    return {
        "id": appointment.id,
        "status": appointment.status
    }