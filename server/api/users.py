import pyotp
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from core.dao.models import get_admin_models_for_user
from core.dao.users import (
    delete_user_full,
    set_user_otp_secret,
    get_user,
    set_user_otp_secret_validated,
)
from core.dao.workspaces import get_admin_workspaces_of_user
from core.schemas.users import User
from core.schemas.utils import Message, OtpUrl, OtpValidation
from dependencies import get_current_active_user

router = APIRouter()


@router.get(
    "/user",
    response_model=User,
    tags=["user"],
)
async def read_user(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve current user's data.
    """
    return current_user


@router.get(
    "/user/delete",
    response_model=Message,
    tags=["user"],
    responses={400: {"description": "Attempting to delete admin."}},
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
            detail="Attempting to delete workspace admin. Set another admin first.",
        )

    # check if user is model admin
    if len(await get_admin_models_for_user(current_user.username)) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempting to delete model admin. Set another admin first.",
        )

    # TODO: check if user is any other admin

    await delete_user_full(current_user.username)

    return JSONResponse(status_code=200, content={"message": "User deleted."})


@router.post(
    "/user/otp/create",
    response_model=OtpUrl,
    tags=["user"],
    responses={},
)
async def user_otp_create(current_user: User = Depends(get_current_active_user)):
    """
    Create an OTP secret for the user. If the user already has an OTP secret,
    the old one will be overridden.
    """

    secret = pyotp.random_base32()
    issuer = "Zebbra"
    name = current_user.username
    url = pyotp.totp.TOTP(secret).provisioning_uri(name=name, issuer_name=issuer)

    await set_user_otp_secret(current_user.username, secret)

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
    """

    user = await get_user(current_user.username)

    if user.otp_secret is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP not set up.",
        )

    totp = pyotp.TOTP(user.otp_secret)
    valid = totp.verify(otp)

    if valid:
        await set_user_otp_secret_validated(current_user.username)

    return OtpValidation(otp=otp, valid=valid)
