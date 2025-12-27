from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Date, Time
from sqlalchemy.orm import relationship
from datetime import datetime

from models.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="requested")
    booking_date = Column(Date, default='1970-01-01')
    booking_time = Column(Time, default='00:00:00')
    # relationship back to user
    patient = relationship(
        "User",
        foreign_keys=[patient_id],
        back_populates="patient_appointments"
    )

    doctor = relationship(
        "User",
        foreign_keys=[doctor_id],
        back_populates="doctor_appointments"
    )