from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from api import users, models, sheets
from api.auth import create_access_token, authenticate_user, get_password_hash
from core.models.token_blacklist import add_to_blacklist
from core.models.users import get_user, create_user
from core.schemas.tokens import Token, BlacklistToken
from core.schemas.users import RegisterUser, UserInDB, User
from core.schemas.utils import Message
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, \
    get_current_active_user_token

app = FastAPI(
    title="Zebbra API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(models.router)
app.include_router(sheets.router)


@app.get(
    "/",
    response_model=Message,
)
async def root():
    """
    Heartbeat endpoint to check if server is running.
    """
    return {"message": "Hello Zebbra!"}


@app.post(
    "/token",
    response_model=Token,
    responses={
        401: {"description": "Incorrect username or password"}
    },
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/logout", response_model=Message)
async def logout(token: str = Depends(get_current_active_user_token)):
    """
    Logout the user who is currently logged in. This invalidates the access
    token.
    """
    await add_to_blacklist(BlacklistToken(**{"access_token": token}))
    return {'message': "Logged out."}


@app.post('/register',
          response_model=User,
          responses={
              409: {"description": "Username already exists"}
          })
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
