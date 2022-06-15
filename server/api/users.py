from fastapi import APIRouter, Depends

from core.schemas.users import User
from dependencies import get_current_active_user

router = APIRouter()


@router.get("/user", response_model=User, tags=["users"])
async def read_user(current_user: User = Depends(get_current_active_user)):
    return current_user
