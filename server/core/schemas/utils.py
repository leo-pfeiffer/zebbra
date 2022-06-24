from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.param_functions import Form


class Message(BaseModel):
    message: str


class OtpUrl(BaseModel):
    url: str
    secret: str
    issuer: str
    name: str


class OtpValidation(BaseModel):
    otp: str
    valid: bool


class OAuth2PasswordRequestFormWithOTP(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: str = Form(),
        password: str = Form(),
        scope: str = Form(default=""),
        client_id: str | None = Form(default=None),
        client_secret: str | None = Form(default=None),
        otp: str | None = Form(default=None),
    ):
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.otp = otp
