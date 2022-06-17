from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.models.token_blacklist import is_token_blacklisted
from core.schemas.tokens import TokenData
from core.schemas.users import User
from core.settings import get_settings
from core.models.users import get_user

settings = get_settings()
SECRET_KEY = settings.dict()['AUTH_SECRET']
ALGORITHM = settings.dict()['AUTH_ALGO']
ACCESS_TOKEN_EXPIRE_MINUTES = settings.dict()['AUTH_TOKEN_EXPIRE']

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_user_token(token: str = Depends(oauth2_scheme)):
    return token
