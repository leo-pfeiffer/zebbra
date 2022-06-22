from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from core.models.users import delete_user_full
from core.models.workspaces import get_admin_workspaces_of_user
from core.schemas.users import User
from core.schemas.utils import Message
from dependencies import get_current_active_user

router = APIRouter()


@router.get(
    "/user",
    response_model=User,
    tags=["users"],
)
async def read_user(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve current user's data.
    """
    return current_user


@router.get(
    "/user/delete",
    response_model=Message,
    tags=["users"],
    responses={
        400: {"description": "Attempting to delete admin."}
    }
)
async def delete_user(current_user: User = Depends(get_current_active_user)):
    """
    Delete a user's account. This requires that the user is not
    admin of any workspace, model etc.
    """

    # check if user is workspace admin
    if len(await get_admin_workspaces_of_user(current_user.username)) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempting to delete admin.",
        )

    # TODO: check if user is any other admin

    await delete_user_full(current_user.username)

    return JSONResponse(status_code=200, content={"message": "User deleted."})

