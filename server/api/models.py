from fastapi import APIRouter, Depends, HTTPException

from core.schemas.models import Model
from core.schemas.users import User
from dependencies import get_current_active_user

router = APIRouter()


@router.get(
    "/model",
    response_model=Model,
    tags=["models"]
)
async def get_model(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve a given model.
    """
    return None

