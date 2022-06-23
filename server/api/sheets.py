from fastapi import APIRouter, Depends, HTTPException

from core.schemas.sheets import Sheet
from core.schemas.users import User
from dependencies import get_current_active_user

router = APIRouter()


@router.get("/sheet", response_model=Sheet, tags=["sheets"])
async def get_sheet(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve a given sheet.
    """
    return None
