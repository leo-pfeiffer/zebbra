from datetime import datetime, date

from bson import ObjectId
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.param_functions import Form

from core.schemas.integrations import IntegrationProvider


class DataPoint(BaseModel):
    id: str
    integration: IntegrationProvider
    name: str


class ExpiredMessage(BaseModel):
    expired: bool


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


class InviteCode(BaseModel):
    invite_code: str
    workspace_id: str
    expires: datetime

    def expired(self):
        return datetime.utcnow() > self.expires


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


class DateString(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str | date):
        if not isinstance(v, str) and not isinstance(v, date):
            raise TypeError("string or datetime.date required")
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"invalid date string format: {v}")
            return cls(v)
        return v.strftime("%Y-%m-%d")

    def to_date(self):
        return datetime.strptime(self, "%Y-%m-%d").date()

    def __repr__(self):
        return f"{super().__repr__()}"


class PyObjectId(ObjectId):
    """
    MongoDB ObjectId converter.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
