import pyotp
from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse

from core.dao.models import get_admin_models_for_user, get_models_for_user
from core.dao.users import (
    delete_user_full,
    set_user_otp_secret,
    get_user,
    set_user_otp_secret_validated,
    update_user_field,
    update_username,
    username_exists,
    get_user_by_username,
)
from core.dao.workspaces import get_admin_workspaces_of_user, get_workspaces_of_user
from core.schemas.users import User, UserInfo
from core.schemas.utils import Message, OtpUrl, OtpValidation
from api.utils.dependencies import get_current_active_user, get_password_hash

router = APIRouter()


@router.get(
    "/user",
    response_model=UserInfo,
    tags=["user"],
)
async def retrieve_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve current user's data.
    """

    # get workspaces of the user
    workspaces = []
    for workspace in await get_workspaces_of_user(current_user.id):
        workspaces.append(
            UserInfo.WorkspaceInfo(**{"name": workspace.name, "_id": str(workspace.id)})
        )

    # get models of the user
    models = []
    for model in await get_models_for_user(current_user.id):
        models.append(
            UserInfo.ModelInfo(**{"name": model.meta.name, "_id": str(model.id)})
        )

    return UserInfo(
        **{
            "_id": str(current_user.id),
            "username": current_user.username,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "workspaces": workspaces,
            "models": models,
        }
    )


@router.delete(
    "/user",
    response_model=Message,
    tags=["user"],
    responses={400: {"description": "Attempting to delete admin."}},
)
async def delete_current(current_user: User = Depends(get_current_active_user)):
    """
    Delete a user's account. This requires that the user is not
    admin of any workspace, model etc.
    """

    # check if user is workspace admin
    if len(await get_admin_workspaces_of_user(current_user.id)) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempting to delete workspace admin. Set another admin first.",
        )

    # check if user is model admin
    if len(await get_admin_models_for_user(current_user.id)) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempting to delete model admin. Set another admin first.",
        )

    await delete_user_full(current_user.id)

    return JSONResponse(status_code=200, content={"message": "User deleted."})


@router.post("/user", response_model=User, tags=["user"])
async def update_current_user(
    username: EmailStr | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    password: str | None = None,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update the current user.
        username: New username (e-mail address)
        first_name: New first name
        last_name: New last name
        password: New password
    """

    # update username
    if username is not None and username != current_user.username:
        # make sure username is not already taken
        if await username_exists(username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )
        await update_username(current_user.id, username)

    # update first name
    if first_name is not None:
        await update_user_field(current_user.id, "first_name", first_name)

    # update last name
    if last_name is not None:
        await update_user_field(current_user.id, "last_name", last_name)

    # update password
    if password is not None:
        hashed_password = get_password_hash(password)
        await update_user_field(current_user.id, "hashed_password", hashed_password)

    # return updated user
    return await get_user(current_user.id)


@router.post(
    "/user/otp/create",
    response_model=OtpUrl,
    tags=["user"],
    responses={},
)
async def create_otp_secret_for_current_user(
    current_user: User = Depends(get_current_active_user),
):
    """
    Create an OTP secret for the user. If the user already has an OTP secret,
    the old one will be overridden.
    """

    secret = pyotp.random_base32()
    issuer = "Zebbra"
    name = current_user.username
    url = pyotp.totp.TOTP(secret).provisioning_uri(name=name, issuer_name=issuer)

    await set_user_otp_secret(current_user.id, secret)

    return OtpUrl(url=url, name=name, issuer=issuer, secret=secret)


@router.post(
    "/user/otp/validate",
    response_model=OtpValidation,
    tags=["user"],
    responses={},
)
async def user_otp_validate(
    otp: str, current_user: User = Depends(get_current_active_user)
):
    """
    Validate an OTP.
        otp: The OTP to validate.
    """

    user = await get_user(current_user.id)

    if user.otp_secret is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP not set up.",
        )

    totp = pyotp.TOTP(user.otp_secret)
    valid = totp.verify(otp)

    if valid:
        await set_user_otp_secret_validated(current_user.id)

    return OtpValidation(otp=otp, valid=valid)


@router.get(
    "/user/requiresOtp",
    response_model=Message,
    tags=["user"],
)
async def check_otp_status_of_current_user(username: str):
    """
    Check if the user requires an OTP.
        username: The username of the user.
    """

    user = await get_user_by_username(username)

    if user is None:
        return {"message": "OTP not required"}

    if user.otp_secret is None or not user.otp_validated:
        return {"message": "OTP not required"}
    else:
        return {"message": "OTP required"}
