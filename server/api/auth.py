from datetime import datetime, timedelta

import pyotp
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt

from core.dao.token_blacklist import add_to_blacklist
from core.dao.users import get_user, create_user
from core.schemas.tokens import Token, BlacklistToken
from core.schemas.users import RegisterUser, UserInDB, User
from core.schemas.utils import Message, OAuth2PasswordRequestFormWithOTP
from dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user_token,
    verify_password,
    get_password_hash,
)
from dependencies import SECRET_KEY, ALGORITHM

router = APIRouter()


async def authenticate_user(username: str, password: str) -> UserInDB | bool:
    user = await get_user(username)
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
    responses={409: {"description": "Username already exists"}},
)
async def register_user(form_data: RegisterUser):
    """
    Register a new user.
    """

    # make sure username is not already taken
    if (await get_user(form_data.username)) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    # convert into UserInDb object
    hashed_password = get_password_hash(form_data.password)

    user_data = form_data.dict()
    user_data["workspaces"] = [user_data["workspaces"]]
    user_data["hashed_password"] = hashed_password
    user_data["disabled"] = False
    new_user = UserInDB(**user_data)

    # insert user
    await create_user(new_user)

    # return user object
    return await get_user(new_user.username)
