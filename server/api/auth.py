from datetime import datetime, timedelta

import pyotp
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from core.dao.invite_codes import get_invite_code, set_used_by
from core.dao.token_blacklist import add_to_blacklist
from core.dao.users import (
    create_user,
    get_user_by_username,
    username_exists,
    add_user_to_workspace,
)
from core.dao.workspaces import (
    workspace_exists,
    create_workspace,
    workspace_name_exists,
)
from core.exceptions import UniqueConstraintFailedException
from core.schemas.tokens import Token, BlacklistToken
from core.schemas.users import RegisterUser, UserInDB, User
from core.schemas.utils import Message, OAuth2PasswordRequestFormWithOTP, ExpiredMessage
from core.schemas.workspaces import Workspace
from dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user_token,
    verify_password,
    get_password_hash,
    decode_token,
)
from dependencies import SECRET_KEY, ALGORITHM

router = APIRouter()


async def authenticate_user(username: str, password: str) -> UserInDB | bool:
    user = await get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post(
    "/token",
    tags=["auth"],
    response_model=Token,
    responses={401: {"description": "Incorrect username or password"}},
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestFormWithOTP = Depends(),
):
    """
    Get an OAuth access token using the user's credentials.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # user has validated 2FA, thus compare the OTP
    if user.otp_validated:
        totp = pyotp.TOTP(user.otp_secret)
        if not totp.verify(form_data.otp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="OTP of Two-Factor Authentication is invalid",
            )

    # create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token/expired", response_model=ExpiredMessage, tags=["auth"])
async def token_expired(token: str = Depends(get_current_active_user_token)):
    expired = False
    try:
        decode_token(token)
    except ExpiredSignatureError:
        expired = True
    return {"expired": expired}


@router.post("/logout", response_model=Message, tags=["auth"])
async def logout(token: str = Depends(get_current_active_user_token)):
    """
    Logout the user who is currently logged in. This invalidates the access
    token.
    """
    await add_to_blacklist(BlacklistToken(**{"access_token": token}))
    return {"message": "Logged out."}


@router.post(
    "/register",
    tags=["auth"],
    response_model=User,
    responses={409: {"description": "Username or workspace already exists"}},
)
async def register_user(form_data: RegisterUser):
    """
    Register a new user. To add the user to an existing workspace, specify the
    workspace_id. To create a new workspace with the user as admin, specify
    new_workspace_name. You cannot specify both.
    """

    # make sure username is not already taken
    if await username_exists(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    use_current_wsp = form_data.invite_code is not None
    create_new_wsp = form_data.new_workspace_name is not None

    workspace_id = None

    if use_current_wsp == create_new_wsp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly one of workspace_id and new_workspace_name must be specified.",
        )

    if create_new_wsp and await workspace_name_exists(form_data.new_workspace_name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workspace name already exists",
        )

    if use_current_wsp:
        invite_code = await get_invite_code(form_data.invite_code)
        if invite_code is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invite code does not exist",
            )
        if invite_code.expired():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invite code has expired",
            )
        if not await workspace_exists(invite_code.workspace_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Workspace does not exist",
            )

        workspace_id = invite_code.workspace_id

    # convert into UserInDb object
    hashed_password = get_password_hash(form_data.password)

    user_data = form_data.dict()
    user_data["hashed_password"] = hashed_password
    user_data["disabled"] = False
    new_user = UserInDB(**user_data)

    # insert user
    res = await create_user(new_user)

    # create workspace
    if create_new_wsp:
        workspace = Workspace(
            name=form_data.new_workspace_name, admin=new_user.id, users=[new_user.id]
        )
        await create_workspace(workspace)

    # add to workspace
    elif use_current_wsp:
        await add_user_to_workspace(res.inserted_id, workspace_id)
        await set_used_by(form_data.invite_code, new_user.id)

    # return user object
    return await get_user_by_username(new_user.username)
