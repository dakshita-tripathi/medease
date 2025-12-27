from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import random

from core.security import hash_password, verify_password
from core.jwt import create_access_token
from models.user import User
from schemas.user import UserRegister, UserLogin, TokenResponse
from core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def add_user(user: UserRegister, db: AsyncSession = Depends(get_db)):
    try:
        db_user = User(
        id=random.randint(1,1000),
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role,
        username=user.username
    )
        result = db.execute(select(User).where(User.email == user.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        raise SystemError('cannot add user')

@router.post("/login")
def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "sub": str(user.id),
        "role": user.role
    }

    access_token = create_access_token(token_data)
    print(user.id)
    return {
        "access_token": access_token
    }