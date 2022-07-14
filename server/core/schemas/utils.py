import re
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
    date_string_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    date_string_regex_compiled = re.compile(date_string_regex)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=cls.date_string_regex,
            examples=["1999-01-25", "2001-04-04"],
        )

    @classmethod
    def validate(cls, v: str | date):
        if not isinstance(v, str) and not isinstance(v, date):
            raise TypeError("string or datetime.date required")
        if isinstance(v, str):
            m = cls.date_string_regex_compiled.fullmatch(v.upper())
            if not m:
                raise ValueError(f"invalid date string format: {v}")
            return cls(v)
        return v.strftime("%Y-%m-%d")

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
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
