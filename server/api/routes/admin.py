from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.deps import get_current_user
from models.user import User
from models.doctor_profile import DoctorProfile
from core.database import get_db

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

router = APIRouter(prefix="/admin", tags=["Admin"])
@router.patch("/doctors/{doctor_user_id}/approve")
def approve_doctor(
    doctor_user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(admin_required),
):
    # 1. Fetch doctor user
    result = db.execute(
        select(User).where(
            User.id == doctor_user_id,
            User.role == "doctor"
        )
    )
    doctor_user = result.scalar_one_or_none()

    if not doctor_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    result = db.execute(
        select(DoctorProfile).where(
            DoctorProfile.user_id == doctor_user.id
        )
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not found"
        )

    # 3. Approve
    if profile.is_approved:
        return {"message": "Doctor already approved"}

    profile.is_approved = True
    db.commit()

    return {
        "message": "Doctor approved successfully",
        "doctor_id": doctor_user.id,
        "username": doctor_user.username
    }