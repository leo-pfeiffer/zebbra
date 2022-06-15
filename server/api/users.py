from fastapi import APIRouter, Depends

from core.schemas.users import User
from dependencies import get_current_active_user

router = APIRouter()


@router.get("/users/me/", response_model=User, tags=["users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/", tags=["users"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]