from fastapi import APIRouter, Depends

from api.deps import get_current_user

router = APIRouter( prefix='/user', tags=["User"])

@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return user
