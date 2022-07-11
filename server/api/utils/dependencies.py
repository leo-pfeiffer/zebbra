from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.dao.token_blacklist import is_token_blacklisted
from core.oauth import OAuth2PasswordBearerURL
from core.schemas.tokens import TokenData
from core.schemas.users import User
from core.settings import get_settings
from core.dao.users import get_user_by_username

settings = get_settings()
SECRET_KEY = settings.dict()["AUTH_SECRET"]
ALGORITHM = settings.dict()["AUTH_ALGO"]
ACCESS_TOKEN_EXPIRE_MINUTES = settings.dict()["AUTH_TOKEN_EXPIRE"]
INVITE_CODE_EXPIRES_MINUTES = settings.dict()["INVITE_CODE_EXPIRE"]

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# regular scheme, token passed in Auth header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# alternative scheme where token is passed as URL query parameter
oauth2_scheme_url = OAuth2PasswordBearerURL(tokenUrl="token")


def decode_token(token):
    """
    Decode a JWT token into username and password
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the currently logged-in user from the provided token.
    """
    blacklist_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if await is_token_blacklisted(token):
        raise blacklist_exception

    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_url(token: str = Depends(oauth2_scheme_url)):
    """
    Get the currently logged-in user from the provided token when the token is passed
    through a URL query param.
    """
    return await get_current_user(token)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Helper method to return the current user, or if the user is inactive, raise an
    exception.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_user_url(
    current_user: User = Depends(get_current_user_url),
):
    """
    Helper method to return the current user, or if the user is inactive, raise an
    exception. Use this method if the token is passed as a URL query param
    """
    return await get_current_active_user(current_user)


async def get_current_active_user_token(token: str = Depends(oauth2_scheme)):
    """
    Return the token of the current user.
    """
    return token


def verify_password(plain_password: str, hashed_password: str):
    """
    Verify a plain password vs its hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """
    Hash a plain password.
    """
    return pwd_context.hash(password)
